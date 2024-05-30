from tests.apps import TestsConfig
from django.urls import path

from tests.views import TestCreateView, TestListView, TestDetailView, TestUpdateView, TestDeleteView, TestRunView, \
    change_published_status, change_published_requested_status, QuestionCreateView, QuestionDetailView, \
    QuestionUpdateView, QuestionDeleteView, AnswersCreateView, AnswersDeleteView, TestCreateMaterialView

app_name = TestsConfig.name

urlpatterns = [
    # View to change published status
    path('view/changepublishedstatus/<str:model>/<int:pk>/', change_published_status,
         name='change_published_status'),

    # View to change some status
    path('view/changepublishedrequestedstatus/<str:model>/<int:pk>/', change_published_requested_status,
         name='change_published_requested_status'),

    # URL pattern for creating a new tests
    path('test_create/', TestCreateView.as_view(), name='test_create'),

    # URL pattern for creating a new tests for special material
    path('test_create/<int:material_pk>/', TestCreateMaterialView.as_view(), name='test_create_for_special_material'),

    # URL pattern for listing tests
    path('', TestListView.as_view(), name='test_list'),

    # URL pattern for viewing a single test
    path('test_view/<int:pk>/', TestDetailView.as_view(), name='test_view'),

    # URL pattern for editing an existing test
    path('test_edit/<int:pk>/', TestUpdateView.as_view(), name='test_edit'),

    # URL pattern for deleting an existing test
    path('test_delete/<int:pk>/', TestDeleteView.as_view(), name='test_delete'),

    # URL pattern for creating a new completed tests
    path('test_run/<int:test_pk>/', TestRunView.as_view(), name='test_run'),

    # URL pattern for creating a new question
    path('question_create/<int:test_pk>/', QuestionCreateView.as_view(), name='question_create'),

    # URL pattern for viewing a single question
    path('question_view/<int:pk>/', QuestionDetailView.as_view(), name='question_view'),

    # URL pattern for editing an existing question
    path('question_edit/<int:pk>/', QuestionUpdateView.as_view(), name='question_edit'),

    # URL pattern for deleting an existing question
    path('question_delete/<int:pk>/<int:test_pk>/', QuestionDeleteView.as_view(), name='question_delete'),

    # URL pattern for creating a new answer
    path('answers_create/<int:question_pk>/', AnswersCreateView.as_view(), name='answers_create'),

    # URL pattern for deleting an existing answer
    path('answers_delete/<int:pk>/<int:question_pk>/', AnswersDeleteView.as_view(), name='answers_delete'),
]
