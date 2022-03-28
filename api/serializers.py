from rest_framework import serializers

from api.models import *


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True)
    project_id = serializers.IntegerField(
        source='id', read_only=True
    )

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author',
                  'author_user_id', 'url']


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True)
    project = serializers.HiddenField(
        default='project'
    )
    project_detail = ProjectSerializer(source='project', read_only=True)
    project_id = serializers.IntegerField(
        source='project.id', read_only=True
    )
    assignee_user_id = serializers.IntegerField(
        source='assignee.id', read_only=True
    )

    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'project',
                  'project_id', 'status', 'author', 'author_user_id',
                  'assignee', 'assignee_user_id', 'created_time',
                  'project_detail']
        extra_kwargs = {'assignee': {'write_only': True}}
