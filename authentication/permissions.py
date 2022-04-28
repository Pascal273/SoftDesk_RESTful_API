from rest_framework import permissions
from rest_framework.exceptions import NotFound

from api.models import Project, Issue


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # write permissions are only allowed to the author
        return obj.author == request.user


class IsContributor(permissions.BasePermission):
    """
    Custom Permission that allows only contributors to access a Project
    or a directly related Object (Issue, ect.)
    """
    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs.keys():
            project_id = view.kwargs['project_pk']
        elif 'pk' in view.kwargs.keys():
            project_id = view.kwargs['pk']
        else:
            return True
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        if request.user in project.contributors.all():
            return True
        return False


class IsRelatedProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a project to add, updated
    or delete a project-related object.
    """
    def has_permission(self, request, view):
        """
        Only the author of the Project is allowed to add (post) a new
        object to it.
        """
        try:
            project = Project.objects.get(id=view.kwargs['project_pk'])
        except Project.DoesNotExist:
            raise NotFound('A Project with that id does not exist')
        if request.user == project.author:
            return True
        return request.method in permissions.SAFE_METHODS


class IsRelatedIssueAuthor(permissions.BasePermission):
    """
    Custom permission to only allow the author of an issue to add a new
    comment.
    """

    def has_permission(self, request, view):
        """
        Only the author of the issue is allowed to add a new comment.
        """
        issue = Issue.objects.get(id=view.kwargs['issue_pk'])
        if request.user == issue.author:
            return True
        return request.method in permissions.SAFE_METHODS


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission that returns True if the user is not authenticated.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True
