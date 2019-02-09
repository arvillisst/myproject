from .models import Article
from snippets.models import Snippet
from django.contrib.sitemaps import Sitemap
from tutorials.models import Tutorial


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created


class SnippetSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Snippet.objects.all()

    def lastmod(self, obj):
        return obj.created

class TutorialSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Tutorial.objects.all()

    def lastmod(self, obj):
        return obj.created