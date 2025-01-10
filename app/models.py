from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

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


# This is the Slider Model
class Slider(models.Model):
    title = models.CharField(max_length=200, help_text="Title for the slider item")
    description = models.TextField(blank=True, help_text="Description for the slider item")
    image = models.ImageField(upload_to='slider_images/', help_text="Upload the image for the slider")
    link = models.URLField(blank=True, null=True, help_text="Optional link for the slider item")
    is_active = models.BooleanField(default=True, help_text="Toggle to display or hide the slider")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the slider item was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the slider item was last updated")

    def __str__(self):
        return self.title

# This is a Card Model
class Card(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the card")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Optional subtitle for the card")
    image = models.ImageField(upload_to='card_images/', blank=True, null=True, help_text="Image for the card")
    description = models.TextField(blank=True, help_text="Description or details for the card")
    link = models.URLField(blank=True, null=True, help_text="Optional link associated with the card")
    is_active = models.BooleanField(default=True, help_text="Toggle to display or hide the card")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the card was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the card was last updated")

    def __str__(self):
        return self.title
    
#This is a Blog Model
class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the blog post")
    slug = models.SlugField(unique=True, help_text="Unique slug for the blog post (auto-generated or manually set)")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', help_text="Author of the blog post")
    content = models.TextField(help_text="Main content of the blog post")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, help_text="Optional image for the blog post")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', help_text="Publication status of the blog post")
    category = models.CharField(max_length=100, blank=True, help_text="Category or tag for the blog post")
    published_at = models.DateTimeField(blank=True, null=True, help_text="Publication date and time of the blog post")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the blog post was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the blog post was last updated")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title
 