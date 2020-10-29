import itertools

from django.db import models
# from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.text import slugify
from .fields import OrderField
from django.contrib.auth import get_user_model

User = get_user_model()


class Subject(models.Model):
    title = models.CharField(max_length=settings.COURSE_TITLE_MAX_LENGTH)
    slug = models.SlugField(
                  max_length=settings.COURSE_TITLE_MAX_LENGTH, 
                  blank=True, 
                  unique=True)

    def save(self, *args, **kwargs):
      if not self.slug:
        self.slug = slugify(self.title)
      
      super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.COURSE_TITLE_MAX_LENGTH)
    slug = models.SlugField(
                            max_length=settings.COURSE_TITLE_MAX_LENGTH,
                            blank=True, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def _generate_slug(self):
      slug_modify = slug_original = slugify(self.title, allow_unicode=True)
      for i in itertools.count(1):
        if not Course.objects.filter(slug=slug_modify).exists():
          break

        slug_modify = '{}-{}'.format(slug_original, i)

      self.slug = slug_modify


    def save(self, *args, **kwargs):
      # if not self.pk:
      self._generate_slug()

      super().save(*args, **kwargs)




class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.COURSE_TITLE_MAX_LENGTH)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
      return render_to_string(
        f'courses/content/{self._meta.model_name}.html',
                          {'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()