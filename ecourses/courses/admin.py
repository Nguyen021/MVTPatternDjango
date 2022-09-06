from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

from django.contrib.auth.models import Permission

from .models import *


# Register your models here.

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class TagInlineLesson(admin.TabularInline):
    model = Lesson.tags.through


class TagAdmin(admin.ModelAdmin):
    inlines = (TagInlineLesson,)


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'content', 'course']
    search_fields = ['subject', 'course__subject']
    list_filter = ['subject', 'course__subject']
    readonly_fields = ['images']

    inlines = (TagInlineLesson,)

    def images(self, obj):
        return mark_safe(
            "<img src='/static/{img_url}' alt='{alt}' width='120px' />".format(img_url=obj.image.name, alt=obj.subject))

    form = LessonForm

    class Media:
        css = {'all': ('/static/css/style.css',)}


# ------------- Lesson Inline ------------
class LessonInlineCourse(admin.StackedInline):
    model = Lesson
    pk_name = 'course'


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInlineCourse, ]


# ------------- Lesson Inline ------------
class CourseAppAdminsite(admin.AdminSite):
    site_header = 'Course Management System'

    def get_urls(self):
        return [
                   path('course-stats/', self.course_stats)
               ] + super().get_urls()

    def course_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count=Count('lesson')).values("id", "subject", "lesson_count")

        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })


admin_site = CourseAppAdminsite("MyApp")

# admin_site.register(Category)
# admin_site.register(Course, CourseAdmin)
# admin_site.register(Lesson, LessonAdmin)
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(User)
admin.site.register(Permission)
