from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Tutorial
from django.views.generic import ListView
from hitcount.views import HitCountDetailView
from blog.mixins import CategoryMixin


class CategoryView(ListView, CategoryMixin):
    """ Страница со списком туториалов """
    model = Category
    template_name = 'tutorials/home-main1.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        article_list = self.model.objects.order_by('created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(article_list, 6)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context


class TutorialDetailView(HitCountDetailView, CategoryMixin):
    """ Страница с детальной информацией """
    template_name = 'tutorials/post-page.html'
    model = Tutorial
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(TutorialDetailView, self).get_context_data(*args, **kwargs)
        context['art'] = self.get_object().category.tutorial_set.all()
        context['article'] = self.get_object()

        # похожие статьи
        article_tags_ids = self.get_object().tags.values_list('id', flat=True)
        similar_articles = self.model.objects.filter(tags__in=article_tags_ids).exclude(id=self.get_object().id)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        context['similar_articles'] = similar_articles

        # следующая и предыдущая статьи
        context['prev_post'] = self.get_object().category.tutorial_set.filter(id__lt=self.object.id).order_by('id').reverse().first()
        context['next_post'] = self.get_object().category.tutorial_set.filter(id__gt=self.object.id).order_by('id').first()
        return context