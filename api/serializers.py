from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.models import *
from authentication.models import User


class ContributorSerializer(serializers.ModelSerializer):
    contributor_id = serializers.IntegerField(
        source='id', read_only=True)
    user_id = serializers.IntegerField(
        source='user.id', read_only=True)
    project_id = serializers.IntegerField(
        source='project.id', read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all())

    def create(self, validated_data):
        """
        Create Methode altered to add the project that matches the PK from URL
        automatically.
        Permission gets added automatically matching the role of the
        contributor.
        """
        project = Project.objects.get(
            id=self.context['view'].kwargs['project_pk'])
        validated_data['project'] = project
        role = validated_data['role']
        if not role:
            validated_data['role'] = 'COLLABORATOR'
        if role == 'AUTHOR':
            validated_data['permission'] = 'manage'
        else:
            validated_data['permission'] = 'edit'
        return Contributor.objects.create(**validated_data)

    class Meta:
        model = Contributor
        fields = ['contributor_id', 'user', 'user_id', 'project_id',
                  'permission', 'role']
        extra_kwargs = {'permission': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    comment_id = serializers.IntegerField(
        source='id', read_only=True)
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True
    )
    issue_id = serializers.IntegerField(
        source='issue.id', read_only=True)

    def create(self, validated_data):
        """
        Create Methode altered to add the issue that matches the PK from URL
        automatically.
        """
        issue = Issue.objects.get(
            id=self.context['view'].kwargs['issue_pk'])
        validated_data['issue'] = issue
        return Comment.objects.create(**validated_data)

    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id',
                  'created_time', 'author']


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.IntegerField(
        source='id', read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True)
    project_id = serializers.IntegerField(default='project.id', read_only=True)
    assignee_user_id = serializers.IntegerField(
        source='assignee.id', read_only=True)
    comments = serializers.SerializerMethodField()  # -> get_comments
    assignee = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all(),
        write_only=True, allow_null=True)

    def get_comments(self, issue):
        """
        Gets representation from CommentSerializer for all the Comment-objects
        that are related to this Issue.
        """
        comments = Comment.objects.filter(issue=issue)
        return CommentSerializer(
            comments, many=True, read_only=True, required=False).data

    def create(self, validated_data):
        """
        Create Methode altered to add the project that matches the PK from URL
        automatically.
        Set the author as the assignee by default if no assignee was
        selected.
        If the selected assignee is not already a contributor of the related
        project it will be added automatically.
        """
        project = Project.objects.get(
            id=self.context['view'].kwargs['project_pk'])
        validated_data['project'] = project
        if not validated_data['assignee']:
            validated_data['assignee'] = validated_data['author']
        if validated_data['assignee'] not in project.contributors.all():
            contributor = Contributor.objects.create(
                user=validated_data['assignee'],
                project=project,
                permission='edit',
                role='COLLABORATOR'
            )
            contributor.save()
        return Issue.objects.create(**validated_data)

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'description', 'tag', 'priority',
                  'project_id', 'status', 'author', 'author_user_id',
                  'assignee', 'assignee_user_id', 'created_time', 'comments']


class ProjectSerializer(NestedHyperlinkedModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True)
    project_id = serializers.IntegerField(
        source='id', read_only=True
    )
    issues = serializers.SerializerMethodField()  # -> get_issues
    contributors = serializers.SerializerMethodField()  # -> get_contributors

    def get_issues(self, project):
        """
        Gets representation from IssueSerializer for all the Issue-objects that
        are related to this project.
        """
        issues = Issue.objects.filter(project=project)
        return IssueSerializer(
            issues, many=True, read_only=True, required=False).data

    def get_contributors(self, project):
        """
        Gets representation from ContributorSerializer for all Contributor-
        objects to serialize the Contributor-table and not the default
        related user.
        """
        contributors = Contributor.objects.filter(project=project)
        return ContributorSerializer(
            contributors, many=True, required=False).data

    def create(self, validated_data):
        """
        Create Methode altered to add the Contributor Table for the author
        automatically.
        """
        project = Project.objects.create(**validated_data)
        contributors = Contributor.objects.create(
            user=validated_data['author'],
            project=project,
            permission='manage',
            role='AUTHOR'
        )
        contributors.save()
        return project

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author',
                  'author_user_id', 'url', 'contributors', 'issues']
