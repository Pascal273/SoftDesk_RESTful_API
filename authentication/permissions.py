from rest_framework import permissions

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
    Custom Permission that allows only contributors to access a Project.
    """
    def has_permission(self, request, view):
        # print(view)
        if 'pk' in view.kwargs.keys():
            project = Project.objects.get(id=view.kwargs['pk'])
            if request.user in project.contributors.all():
                return True
            return False
        return True


class IsRelatedProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a project to add, updated
    or delete new related object.
    """
    def has_permission(self, request, view):
        """
        Only the author of the Project is allowed to add (post) a new
        object to it.
        """
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.user == project.author:
            return True
        if request.method != 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Only the author of the Project is allowed to update or delete
        a related object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        project = obj.project
        return project.author == request.user


class IsRelatedIssueAuthor(permissions.BasePermission):
    """
    Custom permission to only allow the author of a project to add a new
    comment.
    """

    def has_permission(self, request, view):
        """
        Only the author of the issue is allowed to add a new comment.
        """
        issue = Issue.objects.get(id=view.kwargs['issue_pk'])
        if request.user == issue.author:
            return True
        return request.method != 'POST'


class IsRelatedProjectContributor(permissions.BasePermission):
    """
    Custom permission to only allows user that are in the contributor list of
    a project to CRUD Issues.
    """
    def has_permission(self, request, view):
        """
        Only a contributor of a Project is allowed to access instances of it.
        """
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.user in project.contributors.all():
            return True
        # if request.method != 'POST':
        #     return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # write permissions are only allowed to the author
        project = obj.project
        return request.user in project.contributors.all()
