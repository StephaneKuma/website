from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ckeditor.widgets import CKEditorWidget

from .models import Course, Section, Lesson


class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('COURSE SECTION'), {'fields': ['section']}),
        (_('LESSON DESCRIPTION'), {'fields': ['title', 'slug', 'position', 'content']}),
        (_('LESSON VIDEO'), {'fields': ['video_url', 'thumbnail']})
    ]
    list_display = ['section', 'title', 'position', 'video_url']
    list_filter = ['section', 'position']
    search_fields = ['content', 'title', 'position', 'section', 'price']
    list_editable = ['position', 'video_url']


admin.site.register(Lesson, LessonAdmin)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class SectionInline(admin.TabularInline):
    model = Section
    extra = 2


class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('COURSE'), {'fields': ['course']}),
        (_('SECTION'), {'fields': ['position']})
    ]
    inlines = [LessonInline]
    list_filter = ['course']
    search_fields = ['course', 'position']


admin.site.register(Section, SectionAdmin)


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('COURSE'), {'fields': ['title', 'slug', 'image', 'description', 'is_free', 'price']})
    ]
    form = CourseAdminForm
    inlines = [SectionInline]
    list_display = ['title', 'image', 'description', 'is_free', 'price']
    list_filter = ['title', 'is_free', 'price']
    search_fields = ['title', 'description']


admin.site.register(Course, CourseAdmin)
