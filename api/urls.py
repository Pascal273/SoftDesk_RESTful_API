from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

contributor_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
contributor_router.register(
    r'users', views.ContributorViewSet, basename='project-users')

issue_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project',
)
issue_router.register(r'issues', views.IssueViewSet)

comment_router = routers.NestedDefaultRouter(
    issue_router,
    r'issues',
    lookup='issue'
)
comment_router.register(
    r'comments', views.CommentViewSet, basename='issue-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(contributor_router.urls)),
    path('', include(issue_router.urls)),
    path('', include(comment_router.urls)),
]
