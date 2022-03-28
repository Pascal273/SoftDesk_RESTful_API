from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPES = (
        ('back end', 'back end'),
        ('front end', 'front end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=TYPES)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)


class Contributor(models.Model):
    PERMISSIONS = (
        ('read', 'read'),
        ('write', 'write'),
    )
    ROLES = (
        ('AUTHOR', 'AUTHOR'),
        ('GUEST', 'GUEST')
    )

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user')
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE,
                                related_name='project')
    permission = models.CharField(max_length=30, choices=PERMISSIONS)
    role = models.CharField(max_length=30, choices=ROLES)

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    TAGS = (
        ('BUG', 'BUG'),
        ('ENHANCEMENT', 'ENHANCEMENT'),
        ('TASK', 'TASK'),
    )
    PRIORITIES = (
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    )
    STATS = (
        ('To-Do', 'To-Do'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=30, choices=TAGS)
    priority = models.CharField(max_length=30, choices=PRIORITIES)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATS)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 related_name='assignee',
                                 null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=255)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)
    issue = models.ForeignKey(to=Issue,
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
