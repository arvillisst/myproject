from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount



def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return '{0}/{1}'.format(instance, filename)

class Snippet(models.Model, HitCountMixin):
    title = models.CharField(max_length=125)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=generate_filename, blank=True, verbose_name='Фото')
    content = RichTextUploadingField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        verbose_name = 'Сниппет'
        verbose_name_plural = 'Сниппеты'

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('snippet-detail', kwargs={'slug': self.slug})

