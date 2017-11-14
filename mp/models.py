# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from MotionPicture import Document
import uuid
import os
import tarfile
from django.conf import settings
import shutil
from django.contrib.auth.models import User
import json

def project_data_file_path(instance, filename):
    root, ext = os.path.os.path.splitext(filename)
    return u"data_file/{0}_{1}".format(uuid.uuid4(), filename)

class Project(models.Model):

    name = models.CharField(max_length=100, unique=True)
    data_file = models.FileField(upload_to=project_data_file_path)
    video_file = models.FileField(upload_to="video_file/", null=True, default=None)
    main_filename = models.CharField(max_length=255)
    time_line_name = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=20, default=u"Open")
    section_count = models.FloatField(default=1)
    section_unit = models.CharField(
                    max_length=10, default="seg",
                    choices=[["sec", "Seconds"], ["seg", "Segments"]])
    extras = models.TextField(default='{"file_ext": ".webm"}')

    def get_data_file_path(self):
        return  os.path.join(settings.MEDIA_ROOT, self.data_file.name)

    def get_final_video_name(self):
        extras = json.loads(self.extras)
        return "{0}_final{1}".format(self.name, extras.get("file_ext", ".webm"))

    def get_temp_final_video_path(self):
        extras = json.loads(self.extras)
        filename = "{0}_{1}_temp_final{2}".format(self.id, self.name, extras.get("file_ext", ".webm"))
        return os.path.join(settings.MEDIA_ROOT, filename)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

        extract_folder = os.path.join(settings.MEDIA_ROOT, u"extracted")
        extract_folder = os.path.join(extract_folder, u"project_data_{0}".format(self.id))

        if self.segment_set.count():
            return

        src_path = self.get_data_file_path()
        tar_ref = tarfile.open(src_path, "r")
        tar_ref.extractall(extract_folder)

        doc_filename = os.path.join(extract_folder, self.main_filename)
        wh, main_multi_shape = Document.load_and_get_main_multi_shape(doc_filename)

        time_lines = main_multi_shape.timelines
        time_line_name = self.time_line_name
        if time_line_name and time_lines:
            time_line_name = time_lines.keys()[0]
        if time_line_name in time_lines:
            time_line = time_lines[time_line_name]
            duration = time_line.duration

            if self.section_unit == "seg":
                segment_duration = duration*1./self.section_count
            else:
                segment_duration = self.section_count

            start_time = 0
            i=0
            while start_time<duration:
                end_time = min(duration, start_time+segment_duration)
                segment=Segment(project=self, serial=i,
                    start_time=start_time, end_time=end_time)
                segment.save()
                start_time = end_time
                i += 1

        Document.unload_file(doc_filename)
        shutil.rmtree(extract_folder)

    def __str__(self):
        return u"{0}-{1}".format(self.name, self.main_filename)

def project_segment_path(instance, filename):
    return u"project_videos_{0}/{1}_{2}".format(instance.project.id, instance.id, filename)

class Segment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    serial = models.IntegerField(default=0)
    start_time = models.FloatField()
    end_time = models.FloatField()
    status = models.CharField(max_length=20, default=u"Open")
    video_file = models.FileField(upload_to=project_segment_path)
    booked_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_full_video_file_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.video_file.name)

    def __str__(self):
        return u"id:{2}::{0}-{1}".format(self.start_time, self.end_time, self.id)
