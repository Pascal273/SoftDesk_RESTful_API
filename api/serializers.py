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
        default=serializers.CurrentUserDefault())
    author_user_id = serializers.IntegerField(
        source='author.id', read_only=True)
    project_detail = ProjectSerializer(source='project', read_only=True)
    project_id = serializers.IntegerField(default='project.id', read_only=True)
    assignee_user_id = serializers.IntegerField(
        source='assignee.id', read_only=True)

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
        fields = ['title', 'description', 'tag', 'priority',
                  'project_id', 'status', 'author', 'author_user_id',
                  'assignee', 'assignee_user_id', 'created_time',
                  'project_detail']
        extra_kwargs = {'assignee': {'write_only': True}}
