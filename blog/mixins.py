from django.views.generic.base import ContextMixin
from .models import Category, Article
from taggit.models import Tag



class TagMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['category'] = Category.objects.all()
        return context



class CategoryMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path
        context['tags_from_mixin'] = Tag.objects.all()
        context['categories_from_mixin'] = Category.objects.all()
        context['popular_articles'] = Article.objects.order_by('-hit_count_generic__hits')[:5]
        context['all_tags'] = Tag.objects.all()
        context['three_first_articles'] = Article.objects.all().order_by('created')[:3]
        return context