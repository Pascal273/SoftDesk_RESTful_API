from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.models import *


class ContributorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(
        source='user.id', read_only=True)
    project_id = serializers.IntegerField(
        source='project.id', read_only=True)

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']


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
    # project_detail = ProjectSerializer(source='project', read_only=True)
    project_id = serializers.IntegerField(default='project.id', read_only=True)
    assignee_user_id = serializers.IntegerField(
        source='assignee.id', read_only=True)
    comments = serializers.SerializerMethodField()  # -> get_comments

    def get_comments(self, issue):
        """
        Gets representation from CommentSerializer for all the Issue-objects
        that are related to this project.
        """
        comments = Comment.objects.filter(issue=issue)
        return CommentSerializer(
            comments, many=True, read_only=True, required=False).data

    def create(self, validated_data):
        """
        Create Methode altered to add the project that matches the PK from URL
        automatically.
        """
        project = Project.objects.get(
            id=self.context['view'].kwargs['project_pk'])
        validated_data['project'] = project
        return Issue.objects.create(**validated_data)

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'description', 'tag', 'priority',
                  'project_id', 'status', 'author', 'author_user_id',
                  'assignee', 'assignee_user_id', 'created_time', 'comments']
        extra_kwargs = {'assignee': {'write_only': True}}


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
            contributors, many=True, read_only=True, required=False).data

    def create(self, validated_data):
        """
        Create Methode altered to add the Contributor Table for the author
        automatically.
        """
        project = Project.objects.create(**validated_data)
        contributors = Contributor.objects.create(
            user=validated_data['author'],
            project=project,
            permission='write',
            role='AUTHOR'
        )
        contributors.save()
        return project

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author',
                  'author_user_id', 'url', 'contributors', 'issues']
