from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from education_content.models import Chapter, Material, MaterialPhotos


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    # Define how the Chapter model is displayed in the Django admin panel.

    list_filter = ('title',)


@admin.register(Material)
class MaterialAdmin(SummernoteModelAdmin):
    # Define how the Material model is displayed in the Django admin panel.
    list_filter = ('topic',)
    summernote_fields = ('text',)


@admin.register(MaterialPhotos)
class MaterialPhotosAdmin(admin.ModelAdmin):
    # Define how the MaterialPhotos model is displayed in the Django admin panel.

    list_filter = ('signature',)
