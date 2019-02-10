from django.contrib import admin
from .models import Category, Tutorial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'created' )
    list_filter = ['category']
    date_hierarchy = 'created'