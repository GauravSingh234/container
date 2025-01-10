from django.shortcuts import render, get_object_or_404
from .models import Page, ContentContainer,Card,Slider,Blog
from django.contrib.contenttypes.models import ContentType

def page_detail(request, page_slug):
    # Get the Page by slug
    page = get_object_or_404(Page, slug=page_slug)

    # Get all content containers for the page
    containers = ContentContainer.objects.filter(page=page)
    cards = Card.objects.filter(is_active=True)
    sliders = Slider.objects.filter(is_active=True)
    blogs = Blog.objects.filter(status="published").order_by('-published_at')[:5]  # Fetch latest 5 blogs
    # print(containers,"///////////////")

    # Create a context to send the page and containers to the template
    context = {
        'page': page,
        'containers': containers,
        'cards': cards,
        'sliders': sliders,
        'blogs': blogs,
    }

    return render(request, 'page-detail.html', context)
