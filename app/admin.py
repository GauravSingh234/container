from django.contrib import admin
from .models import TeamMember, TeamSection, Page, PageSection, ContentContainer

# Admin for TeamMember
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'photo', 'bio')
    search_fields = ('name', 'role')
    list_filter = ('role',)

admin.site.register(TeamMember, TeamMemberAdmin)

# Admin for TeamSection
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'member')
    search_fields = ('title', 'member__name')
    list_filter = ('order',)

admin.site.register(TeamSection, TeamSectionAdmin)

# Admin for PageSection (Intermediate model)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'section', 'order')
    search_fields = ('page__title', 'section__title')
    list_filter = ('order',)

admin.site.register(PageSection, PageSectionAdmin)

# Admin for ContentContainer
class ContentContainerAdmin(admin.ModelAdmin):
    list_display = ('page',  'title', 'content', 'get_content_display',)
    search_fields = ('title', 'content')
    # list_filter = ('container_type',)
    
    # Use a custom method to display the content in the admin (it may display HTML or plain text)
    def get_content_display(self, obj):
        return obj.get_content_display()
    get_content_display.short_description = 'Content Display'

admin.site.register(ContentContainer, ContentContainerAdmin)


# Admin for Page
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'get_sections')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    # filter_horizontal = ('sections',)

    # Custom method to display the sections in the page admin
    def get_sections(self, obj):
        return ", ".join([section.title for section in obj.sections.all()])
    get_sections.short_description = 'Sections'

admin.site.register(Page, PageAdmin)
