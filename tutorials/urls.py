from django.urls import path
from . import views

urlpatterns = [
    path('tutorials/', views.CategoryView.as_view(), name='tutorials'),
    path('tutorials/<slug:category_slug>/<slug:slug>/', views.TutorialDetailView.as_view(), name='tutorial_detail'),
]