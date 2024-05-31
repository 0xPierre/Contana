from django.contrib import admin
from apps.documents.models import Document, DocumentSection, TemplateCategory, Template

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentSection)
admin.site.register(TemplateCategory)
admin.site.register(Template)