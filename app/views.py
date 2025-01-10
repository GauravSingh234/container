from django.shortcuts import render, get_object_or_404
from .models import Page, ContentContainer
from django.contrib.contenttypes.models import ContentType

def page_detail(request, page_slug):
    # Get the Page by slug
    page = get_object_or_404(Page, slug=page_slug)

    # Get all content containers for the page
    containers = ContentContainer.objects.filter(page=page)

    # Create a context to send the page and containers to the template
    context = {
        'page': page,
        'containers': containers
    }

    return render(request, 'page-detail.html', context)
