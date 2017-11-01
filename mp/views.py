# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from . import models
import mimetypes
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import django.contrib.auth as auth
import json

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return JsonResponse(dict(result="success"))
    return JsonResponse(dict(result="failed"))

@login_required
def project_info(request, name):
    query = models.Project.objects.filter(name=name)
    if query.count():
        project = query.get()
    else:
        project = models.Project()
    return JsonResponse(dict(
        id=project.id,
        main_filename=project.main_filename,
        time_line_name=project.time_line_name,
        data_file_name=project.data_file.name.split("/")[-1],
        extras = json.loads(project.extras)
    ))

@login_required
def project_data_file(request, name):
    query = models.Project.objects.filter(name=name)
    if query.count():
        project = query.get()
        data_file_path = project.get_data_file_path()
        response = FileResponse(open(data_file_path, "rb"))
        response["Content-Length"] = project.data_file.size
        response["Content-Type"] = "application/octet-stream"
        return response
    return HttpResponseNotFound()

@login_required
def book_open_segment(request, project_name):
    query = models.Project.objects.filter(name=project_name)
    if query.count():
        project = query.get()
        with transaction.atomic():
            segments = models.Segment.objects.select_for_update().filter(
                project=project, status=u"Open").order_by("serial")
            if segments.count()>0:
                segment = segments[0]
                segment.status = u"Booked"
                segment.booked_by = request.user
                segment.booked_at = timezone.now()
                segment.save()
                return JsonResponse(dict(
                    id=segment.id, serial=segment.serial,
                    start_time=segment.start_time, end_time=segment.end_time
                ))
    return JsonResponse(dict())


@csrf_exempt
@login_required
def upload_segment_video(request, project_name, segment_id):
    query = models.Project.objects.filter(name=project_name)
    result = "failed"

    if query.count():
        project = query.get()
        segments = project.segment_set.filter(id=segment_id)
        if segments.count():
            segment = segments[0]
            if segment.status == u"Booked" and segment.booked_by == request.user:
                uploaded_file = request.FILES.get('video')
                if  uploaded_file and uploaded_file.size>0:
                    segment.video_file = uploaded_file
                    segment.status = u"Made"
                    segment.uploaded_at = timezone.now()
                    segment.save()
                    result = "success"
    return JsonResponse(dict(result=result))
