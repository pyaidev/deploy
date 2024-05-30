from django.urls import path

from education_content.apps import EducationContentConfig
from education_content.views import ChapterCreateView, ChapterListView, ChapterDetailView, ChapterUpdateView, \
    ChapterDeleteView, change_published_status, change_published_requested_status, MaterialCreateView, \
    MaterialCreateChapterView, MaterialListView, MaterialDetailView, MaterialUpdateView, MaterialDeleteView, \
    MaterialPhotosCreateMaterialView, MaterialPhotosCreateView, MaterialPhotosListView, MaterialPhotosDetailView, \
    MaterialPhotosDeleteView

app_name = EducationContentConfig.name

urlpatterns = [
    # URL pattern for creating a new chapter
    path('chapter_create/', ChapterCreateView.as_view(), name='chapter_create'),

    # URL pattern for listing chapter with a 60-second cache timeout
    path('', ChapterListView.as_view(), name='chapter_list'),

    # URL pattern for viewing a single chapter
    path('chapter_view/<int:pk>/', ChapterDetailView.as_view(), name='chapter_view'),

    # URL pattern for editing an existing chapter
    path('chapter_edit/<int:pk>/', ChapterUpdateView.as_view(), name='chapter_edit'),

    # URL pattern for deleting an existing chapter
    path('chapter_delete/<int:pk>/', ChapterDeleteView.as_view(), name='chapter_delete'),

    # View to change published status
    path('view/changepublishedstatus/<str:model>/<int:pk>/', change_published_status,
         name='change_published_status'),

    # View to change some status
    path('view/changepublishedrequestedstatus/<str:model>/<int:pk>/', change_published_requested_status,
         name='change_published_requested_status'),

    # URL pattern for creating a new material
    path('material_create/', MaterialCreateView.as_view(), name='material_create'),

    # URL pattern for creating a new material to special chapter
    path('material_create/<int:chapter_pk>/', MaterialCreateChapterView.as_view(),
         name='material_create_for_special_chapter'),

    # URL pattern for listing material with a 60-second cache timeout
    path('material_list/', MaterialListView.as_view(), name='material_list'),

    # URL pattern for viewing a single material
    path('material_view/<int:pk>/', MaterialDetailView.as_view(), name='material_view'),

    # URL pattern for editing an existing material
    path('material_edit/<int:pk>/', MaterialUpdateView.as_view(), name='material_edit'),

    # URL pattern for deleting an existing material
    path('material_delete/<int:pk>/', MaterialDeleteView.as_view(), name='material_delete'),

    # URL pattern for creating a new material to special chapter
    path('materialphotos_create/<int:material_pk>/', MaterialPhotosCreateMaterialView.as_view(),
         name='materialphotos_create_for_special_material'),

    # URL pattern for creating a new materialphoto
    path('materialphotos_create/', MaterialPhotosCreateView.as_view(), name='materialphotos_create'),

    # URL pattern for listing materialphotos with a 60-second cache timeout
    path('materialphotos_list/', MaterialPhotosListView.as_view(), name='materialphotos_list'),

    # URL pattern for deleting an existing materialphoto
    path('materialphotos_delete/<int:pk>/', MaterialPhotosDeleteView.as_view(), name='materialphotos_delete'),

]
