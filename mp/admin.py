# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Project, Segment

class SegmentInline(admin.TabularInline):
    model = Segment
    fields = ('serial', 'status', 'booked_by', 'video_file', 'booked_at', 'uploaded_at')
    readonly_fields = ('video_file', 'booked_by', 'serial', 'booked_at', 'uploaded_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProjectAdmin(admin.ModelAdmin):
    inlines = [SegmentInline]
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.segment_set.count():
            fields= [u'section_count', u'section_unit']
        else:
            fields = []
        fields.append(u"video_file")
        return fields

admin.site.register(Project, ProjectAdmin)
