from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField


class Technology(models.Model):
    """ Save technologies available on the site """

    title = models.CharField(verbose_name=_('title of the tech'), max_length=120)
    slug = models.SlugField(verbose_name=_('tech slug'))
    image = models.ImageField(verbose_name=_('tech image'), default='default.png')
    description = RichTextField(verbose_name=_('description'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:tech-detail', kwargs={'slug': self.slug})

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def courses(self):
        return self.course_set.all().order_by('position')

    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')


class Course(models.Model):
    """ Save courses on technologies available on the site """

    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, verbose_name=_('belongs to'))
    position = models.IntegerField(verbose_name=_('course number'))
    title = models.CharField(verbose_name=_('title of the course'), max_length=120)
    slug = models.SlugField(verbose_name=_('course slug'))
    image = models.ImageField(verbose_name=_('course image'), default='default.png')
    # image = RichTextUploadingField(verbose_name=_('course image'), default='default.png')
    description = models.TextField(verbose_name=_('description'))
    is_free = models.BooleanField(verbose_name=_('course is free ?'), default=True)
    price = models.IntegerField(verbose_name=_('price of the course'), null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def sections(self):
        return self.section_set.all().order_by('position')

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class Section(models.Model):
    """ Save course section """

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name=_('section belongs to'))
    position = models.IntegerField(verbose_name=_('section number'))
    title = models.CharField(verbose_name=_('title of the section'), max_length=100, null=True)

    def __str__(self):
        return '%s - Section %s' % (self.course, self.position)

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class Lesson(models.Model):
    """ Save lessons for available technologies courses on the site """

    slug = models.SlugField(verbose_name=_('lesson slug'))
    title = models.CharField(verbose_name=_('lesson title'), max_length=120)
    # course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True,
                                verbose_name=_('lesson belongs to'))
    position = models.IntegerField(verbose_name=_('course position in the section'))
    content = RichTextField(verbose_name=_('Content of the lesson'), null=True)
    video_url = models.CharField(max_length=200, verbose_name=_('link to the video of the course'))
    thumbnail = models.ImageField(verbose_name=_('thumbnail of the course video'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail', kwargs={
            'course_slug': self.section.course.slug,
            'lesson_slug': self.slug
        })

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
