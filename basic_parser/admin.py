from django.contrib import admin
from basic_parser.models import Profile, Skills
# Register your models here.

class SkillsInline(admin.TabularInline):
    model = Profile.skills.through
    extra = 0

class SkillsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Skills, SkillsAdmin)

class ProfileAdmin(admin.ModelAdmin):
    inlines = [SkillsInline,]
    fieldsets = [
        ('General Information', {'fields': ['name', 'title', 'summary']}),
        ('Contact information', {'fields': ['email', 'phone', 'im', 'advice_to_connect', 'address'], 'classes': ['collapse']}),
    ]

admin.site.register(Profile, ProfileAdmin)