from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from .models import Category, Course, Lesson, Tag
from courses import dao

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'COURSES MANAGE SYSTEM'

    def get_urls(self):
        return [
                   path('course-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()

        stats = Course.objects \
        .annotate(lesson_count=Count('category__id')) \
        .values('id', 'subject', 'lesson_count')
        return TemplateResponse(request,
                            'admin/stats.html', {
                                'course_count': dao.count_course_by_cate()
                            })


admin_site = CourseAppAdminSite(name='myadmin')


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    readonly_fields = ['img']

    def img(self, course):
        if (course):
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                .format(url=course.image.name)
            )


admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Tag)