from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from .serializers import *
from authentication.permissions import (
    IsContributor,
    IsAuthorOrReadOnly,
    IsRelatedIssueAuthor,
    IsRelatedProjectContributor,
    IsRelatedProjectAuthorOrReadOnly,
)

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed.
    """
    queryset = Project.objects.all().order_by('title')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly,
                          IsContributor]

    def get_queryset(self, *args, **kwargs):
        """Show only Project in which the User is a contributor."""
        user = self.request.user
        projects = self.queryset.filter(contributors=user)
        return projects

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        project = self.get_object()
        project.delete()
        return Response({'message': 'project has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contributor-tables to be viewed.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsRelatedProjectAuthorOrReadOnly,
                          IsRelatedProjectContributor]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        return self.queryset.filter(project=project)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        contributor = self.get_object()
        contributor.delete()
        return Response({'message': 'contributor has been deleted'})


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly,
                          IsRelatedProjectContributor]

    def get_serializer_context(self):
        context = super(IssueViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get('project_pk')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        return self.queryset.filter(project=project)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        issue = self.get_object()
        issue.delete()
        return Response({'message': 'issue has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly,
                          IsRelatedIssueAuthor, IsRelatedProjectContributor]

    def get_queryset(self, *args, **kwargs):
        issue_id = self.kwargs.get('issue_pk')
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise NotFound('A Issue with that id does not exist')
        return self.queryset.filter(issue=issue)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        comment = self.get_object()
        comment.delete()
        return Response({'message': 'comment has been deleted'})
