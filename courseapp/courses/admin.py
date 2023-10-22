from django.contrib import admin
from .models import Category
from .models import Course


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Category, LessonAdmin)
admin.site.register(Course)