from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^project/(?P<name>[\S]+)/info$', views.project_info),
    url(r'^project/(?P<name>[\S]+)/data_file$', views.project_data_file),
]
