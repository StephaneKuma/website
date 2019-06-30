from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from ckeditor.widgets import CKEditorWidget

from .models import Course, Section, Lesson


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


admin.site.register(Section, SectionAdmin)


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('COURSE'), {'fields': ['title', 'slug', 'image', 'description']})
    ]
    form = CourseAdminForm
    inlines = [SectionInline]


admin.site.register(Course, CourseAdmin)
