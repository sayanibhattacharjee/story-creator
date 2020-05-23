from django.urls import re_path

from stories import views

urlpatterns = [
    re_path('^create-story/$', views.UploadStoryView.as_view(), name='create_story'),
]
