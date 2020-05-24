from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static


from stories import views

urlpatterns = [
    re_path('^create-story/$', views.UploadStoryView.as_view(), name='create_story'),
    re_path('^all-stories/$', views.AllStoriesView.as_view(), name='all_stories'),
    re_path('^create-story/$', views.UploadStoryView.as_view(), name='create_story'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
