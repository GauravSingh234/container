from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Model 1: TeamMember
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Model 2: TeamSection (with ForeignKey to TeamMember)
class TeamSection(models.Model):
    title = models.CharField(max_length=100)
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='team_sections' , null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of the section display")

    def __str__(self):
        return self.title


# Model 3: Page (to contain multiple containers like Team, Sliders, Images, etc.)
class Page(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the page")
    sections = models.ManyToManyField(TeamSection, blank=True, related_name='pages', through='PageSection')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title


# Model 4: PageSection (through model to organize sections in order)
class PageSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    section = models.ForeignKey(TeamSection, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="The order of this section within the page")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} in {self.page.title}"


# Model 5: ContentContainer (to allow different types of content like Team, Slider, etc.)
class ContentContainer(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    
    # This will point to different models dynamically.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Dynamic model reference
    object_id = models.PositiveIntegerField()  # ID of the object
    content_object = GenericForeignKey('content_type', 'object_id')  # The actual object (like Team, Slider, etc.)

    title = models.CharField(max_length=200, help_text="Title of the container")
    content = models.TextField(help_text="Content or HTML for the container")

    def __str__(self):
        return f"{self.content_type.model} container in {self.page.title}"

    def get_content_display(self):
        return self.content  # This could be extended to handle HTML content or specific rendering logic.
