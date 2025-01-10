from django.urls import path
from . import views

urlpatterns = [
    path('page/<slug:page_slug>/', views.page_detail, name='page_detail'),
]
