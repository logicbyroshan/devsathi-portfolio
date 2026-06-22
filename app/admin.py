from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import (
    Project, Skill, Experience, Blog, ProjectImage, Feature, Learning, FAQ, ContactMessage, Resume
)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at")

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class LearningInline(admin.TabularInline):
    model = Learning
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "categories", "publication_date", "slug")
    list_filter = ("categories", "publication_date")
    search_fields = ("title", "description", "categories")
    inlines = [ProjectImageInline, FeatureInline, LearningInline]  

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "image")

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "project")
    search_fields = ("title",)

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    list_display = ("paragraph", "project")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    list_display = ("title", "categories", "publication_date", "slug")  
    list_filter = ("categories", "publication_date")
    search_fields = ("title", "content", "categories")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "status", "categories")
    list_filter = ("status", "level")
    search_fields = ("name", "categories")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "categories")
    list_filter = ("start_date", "end_date")
    search_fields = ("title", "description", "categories")

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "categories", "created_at")
    list_filter = ("categories", "created_at")
    search_fields = ("question", "answer")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
