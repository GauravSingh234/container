from django.contrib import admin
from .models import TeamMember, TeamSection, Page, PageSection, ContentContainer,Slider,Card,Blog


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'photo', 'bio')
    search_fields = ('name', 'role')
    list_filter = ('role',)


# Admin for TeamSection
@admin.register(TeamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'member')
    search_fields = ('title', 'member__name')
    list_filter = ('order',)


# Admin for PageSection (Intermediate model)
@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('page', 'section', 'order')
    search_fields = ('page__title', 'section__title')
    list_filter = ('order',)


class ContentContainerInline(admin.TabularInline):
    model = ContentContainer
    extra = 1


# Admin for ContentContainer
@admin.register(ContentContainer)
class ContentContainerAdmin(admin.ModelAdmin):
    list_display = ('page',  'title', 'content', 'get_content_display','content_type' ,'order' )
    search_fields = ('title', 'content')
    # list_filter = ('container_type',)
    # inlines=[ContentContainerInline]
    
    # Use a custom method to display the content in the admin (it may display HTML or plain text)
    def get_content_display(self, obj):
        return obj.get_content_display()
    get_content_display.short_description = 'Content Display'



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


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('-created_at',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'created_at', 'published_at', 'author')
    search_fields = ('title', 'content', 'category')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)    