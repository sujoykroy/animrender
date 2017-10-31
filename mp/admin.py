# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Project, Segment

class SegmentInline(admin.TabularInline):
    model = Segment
    fields = ('status', 'machine', 'video_file')
    readonly_fields = ('video_file', 'machine')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProjectAdmin(admin.ModelAdmin):
    inlines = [SegmentInline]
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.segment_set.count():
            return [u'section_count', u'section_unit']
        else:
            return []

admin.site.register(Project, ProjectAdmin)
