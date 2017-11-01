from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^project/(?P<name>[\S]+)/info$', views.project_info),
    url(r'^project/(?P<name>[\S]+)/data_file$', views.project_data_file),
    url(r'^project/(?P<project_name>[\S]+)/book$', views.book_open_segment),
    url(r'^project/(?P<project_name>[\S]+)/segment/(?P<segment_id>[\d]+)/upload$', views.upload_segment_video),
]
