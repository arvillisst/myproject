from django.urls import path
from . import views


urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('tag/<slug>/', views.TagIndexView.as_view(), name='tagged'),
    path('snippets/', views.SnippetListView.as_view(), name='snippets'),
    path('snippets/<slug>/', views.SnippetDetailView.as_view(), name='snippet-detail'),
    path('category/<slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<category>/<slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('search/', views.SearchArticleView.as_view(), name='search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('archive/', views.ArchiveArticleView.as_view(), name='article_archive'),

]