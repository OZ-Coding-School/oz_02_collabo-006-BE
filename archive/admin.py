from django.contrib import admin
from archive.models import Archive, ArchiveStatus, ArchivePost
# Register your models here.

admin.site.register(Archive)
admin.site.register(ArchiveStatus)
admin.site.register(ArchivePost)
