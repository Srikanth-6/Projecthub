from django.contrib import admin
from projects.models import Projects,Review,Tag
# Register your models here.
admin.site.register(Projects)
admin.site.register(Review)
admin.site.register(Tag)