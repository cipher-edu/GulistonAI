from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('add-shartnoma/', add_shartnoma, name='add_shartnoma'),
    path('success/', shartnoma_success, name='shartnoma_success'),
    path('shartnoma/<str:unique_id>/', ShartnomaDetailView.as_view(), name='shartnoma_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)