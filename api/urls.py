from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from api import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
