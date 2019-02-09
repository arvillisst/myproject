from django.db.models import Count
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.dates import ArchiveIndexView
from hitcount.views import HitCountDetailView
from .models import Category, Article
from snippets.models import Snippet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .mixins import TagMixin, CategoryMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm


class CategoryListView(ListView, CategoryMixin):
    template_name = 'blog/home-main1.html'
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(category__name='Django').order_by('-created')
        context['articles_all'] = Article.objects.all().order_by('-created')
        context['all_tags'] = Tag.objects.all()

        article_list = Article.objects.filter(category__name='Django').order_by('-created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(article_list, 4)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context



class CategoryDetailView(HitCountDetailView, CategoryMixin):
    template_name = 'blog/category-detail.html'
    model = Category
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['category'] = self.get_object()
        context['articles_by_category'] = self.get_object().article_set.all()

        cats_list = self.get_object().article_set.all().order_by('-created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(cats_list, 4)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context



class ArticleDetailView(HitCountDetailView, CategoryMixin):
    template_name = 'blog/post-page.html'
    model = Article
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['article'] = self.get_object()

        # похожие статьи
        article_tags_ids = self.get_object().tags.values_list('id', flat=True)
        similar_articles = self.model.objects.filter(tags__in=article_tags_ids).exclude(id=self.get_object().id)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        context['similar_articles'] = similar_articles

        # следующая и предыдущая статьи
        context['prev_post'] = self.get_object().category.article_set.filter(id__lt=self.object.id).order_by('id').reverse().first()
        context['next_post'] = self.get_object().category.article_set.filter(id__gt=self.object.id).order_by('id').first()
        return context


# tags Article
class TagIndexView(ListView, TagMixin, CategoryMixin):
    template_name = 'blog/tags.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        # context['object_list'] = Article.objects.filter(tags__slug=self.kwargs.get('slug'))
        context['categories'] = Category.objects.all()

        object_list = Article.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-created')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(object_list, 4)
        try:
            context['cats'] = paginator.page(page)
        except PageNotAnInteger:
            context['cats'] = paginator.page(1)
        except EmptyPage:
            context['cats'] = paginator.page(paginator.num_pages)
        return context



class SnippetListView(ListView, CategoryMixin):
    template_name = 'blog/snippets.html'
    model = Snippet

    def get_context_data(self, *args, **kwargs):
        context = super(SnippetListView, self).get_context_data(*args, **kwargs)
        context['snippets_all'] = self.model.objects.all()
        return context


class SnippetDetailView(HitCountDetailView, CategoryMixin):
    template_name = 'blog/snippet-detail.html'
    model = Snippet
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(SnippetDetailView, self).get_context_data(*args, **kwargs)
        context['snippets'] = self.model.objects.all()
        context['snippet'] = self.get_object()

        # следующая и предыдущая статьи
        context['prev_post'] = self.model.objects.filter(id__lt=self.object.id).order_by('id').reverse().first()
        context['next_post'] = self.model.objects.filter(id__gt=self.object.id).order_by('id').first()
        return context



class AboutView(TemplateView, CategoryMixin):
    template_name = 'blog/about.html'


class ArchiveArticleView(ArchiveIndexView, CategoryMixin):
    model = Article
    template_name = 'blog/archive.html'
    date_field = 'created'



class SearchArticleView(ListView, CategoryMixin):
    model = Article
    template_name = 'blog/search.html'
    form = SearchForm()
    query = None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchArticleView, self).get_context_data(*args, **kwargs)
        if 'query' in self.request.GET:
            self.form = SearchForm(self.request.GET)
            if self.form.is_valid():
                self.query = self.form.cleaned_data['query']
                search_vector = SearchVector('title', 'content')
                search_query = SearchQuery(self.query)
                # context['results'] = self.model.objects.annotate(search=search_vector,
                #                                    rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank') \
                #                      or Snippet.objects.annotate(search=SearchVector('title', 'content'),).filter(search=search_query)
                results = self.model.objects.annotate(search=search_vector,
                                                                 rank=SearchRank(search_vector, search_query)).filter(
                    search=search_query).order_by('-rank') \
                                     or Snippet.objects.annotate(search=SearchVector('title', 'content'), ).filter(
                    search=search_query)
                page = self.request.GET.get('page', 1)
                paginator = Paginator(results, 3)
                try:
                    context['results'] = paginator.page(page)
                except PageNotAnInteger:
                    context['results'] = paginator.page(1)
                except EmptyPage:
                    context['results'] = paginator.page(paginator.num_pages)
                context['query'] = self.query
        return context