from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from api import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

issue_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
issue_router.register(r'issues', views.IssueViewSet, basename='project-issue')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(issue_router.urls)),
]
