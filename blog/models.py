import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tinymce import HTMLField


User = get_user_model()


class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Category(models.Model):
    title = models.CharField(verbose_name=_('category name'), max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Post(models.Model):
    title = models.CharField(verbose_name=_("article title"), max_length=100)
    overview = models.TextField(verbose_name=_("post overview"))
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField(null=True)
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("edited by"))
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category, verbose_name=_("post belongs to"))
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('blog:post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('blog:post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.timestamp <= now

    was_published_recently.admin_order_field = 'timestamp'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently ?'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.timestamp <= now

    was_published_recently.admin_order_field = 'timestamp'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently ?'


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
