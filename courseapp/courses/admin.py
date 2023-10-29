from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import Category, Course, Lesson, Tag


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Tag)