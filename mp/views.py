# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from . import models
import mimetypes

def project_info(request, name):
    query = models.Project.objects.filter(name=name)
    if query.count():
        project = query.get()
    else:
        project = models.Project()
    return JsonResponse(dict(
        main_filename=project.main_filename,
        time_line_name=project.time_line_name,
        data_file_name=project.data_file.name
    ))

def project_data_file(request, name):
    query = models.Project.objects.filter(name=name)
    if query.count():
        project = query.get()
        data_file_path = project.get_data_file_path()
        return FileResponse(open(data_file_path, "rb"))
    return HttpResponseNotFound()


def book_open_segment(request, project_name, machine):
    query = models.Project.objects.filter(name=name)
    if query.count():
        project = query.get()
        return JsonResponse(dict())
    else:
        return JsonResponse(dict())

