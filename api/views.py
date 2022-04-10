from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import *
from authentication.permissions import *

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed.
    """
    queryset = Project.objects.all().order_by('title')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsRelatedProjectAuthor]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        return self.queryset.filter(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().select_related('project')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly,
                          IsContributorOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        return self.queryset.filter(project=project)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('issue')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly,
                          IsRelatedIssueAuthor]

    def get_queryset(self, *args, **kwargs):
        issue_id = self.kwargs.get('issue_pk')
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise NotFound('A Issue with that id does not exist')
        return self.queryset.filter(issue=issue)
