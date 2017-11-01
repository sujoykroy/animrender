from django.core.management.base import BaseCommand, CommandError
from mp.models import Project
from django.db.models import Q
from moviepy.editor import VideoFileClip, concatenate_videoclips
from MotionPicture import *
from django.core.files import File

class Command(BaseCommand):
    help = 'Build final video of project'

    def add_arguments(self, parser):
        parser.add_argument('project', nargs='?', type=unicode)

    def handle(self, *args, **options):
            project_name = options['project']
            if project_name:
                projects = Project.objects.filter(name=project_name)
            else:
                projects = Project.objects.all()

            if projects.count():
                for project in projects:
                    if project.status == "Made":
                        continue
                    segments = project.segment_set.filter(Q(status=u"Booked")|Q(status=u"Open"))
                    if segments.count() == 0:
                        print("Building final video of {0}".format(project.name))
                        segments = project.segment_set.order_by("serial")
                        clips = []
                        for segment in segments:
                            clip = VideoFileClip(segment.get_full_video_file_path())
                            clip = clip.subclip(0, clip.duration)
                            clips.append(clip)
                        main_clip = concatenate_videoclips(clips)
                        temp_path = project.get_temp_final_video_path()
                        main_clip.write_videofile(
                            temp_path,
                            ffmpeg_params=Document.FFMPEG_PARAMS.split(" "),
                            codec = Document.CODEC, preset="superslow",
                            bitrate = Document.BIT_RATE)

                        project.status = u"Made"
                        f = open(temp_path, "r")
                        project.video_file.save(
                            project.get_final_video_name(), File(f))
                        f.close()
                        project.save()
                        os.remove(temp_path)
                        self.stdout.write(self.style.SUCCESS(
                            "Successfully made final video of {0}".format(project.name)))
                        break
