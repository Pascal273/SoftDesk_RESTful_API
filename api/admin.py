from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Contributor)
admin.site.register(Comment)
