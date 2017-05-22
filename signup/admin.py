from django.contrib import admin
from .models import Document,CoverImages

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'img']


admin.site.register(Document)
admin.site.register(CoverImages, ImageAdmin)

