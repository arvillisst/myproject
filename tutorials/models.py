from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager
from .utils import slugify

def generate_filename_cat(instance, filename):
    filename = instance.slug + '.jpg'
    return '{0}/{1}'.format(instance, filename)


class Category(models.Model):
    name = models.CharField(max_length=120)
    short_description = models.TextField('Краткое описание', max_length=500)
    image = models.ImageField(upload_to=generate_filename_cat, blank=True, verbose_name='Фото')
    slug = models.SlugField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, 120)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'category_slug': self.slug})


def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return '{0}/{1}'.format(instance, filename)

class Tutorial(models.Model, HitCountMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=125, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=generate_filename, blank=True, verbose_name='Фото')
    content = RichTextUploadingField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    tags = TaggableManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, 120)
        super(Tutorial, self).save(*args, **kwargs)

    def __str__(self):
        return 'Статья {0} из категории {1}'.format(self.title, self.category.name)

    def get_absolute_url(self):
        return reverse('tutorial_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})


