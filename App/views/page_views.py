"""
General page views - About, Blog, Contact, FAQ, etc.
"""
from django.shortcuts import render, get_object_or_404

from App.models import Blog


def about_us(request):
    """About us page"""
    return render(request, 'pages/about-us.html')


def notFound(request):
    """404 error page"""
    return render(request, 'pages/404.html')


def checkout(request):
    """Checkout page"""
    return render(request, 'pages/checkout.html')


def blog(request):
    """Blog listing page"""
    return render(request, 'pages/blog.html')


def blog_list_or_default(request):
    """Blog list or default view"""
    blogs = Blog.objects.all()
    return render(request, 'pages/blog-detail.html', {'blogs': blogs})


def blog_detail(request, title):
    """Blog detail page by title/slug"""
    blog = get_object_or_404(Blog, slug=title)
    return render(request, 'pages/blog-detail.html', {'blog': blog})


def privacy(request):
    """Privacy policy page"""
    return render(request, 'pages/privacy.html')


def pricing(request):
    """Pricing page"""
    return render(request, 'pages/pricing.html')


def faq(request):
    """FAQ page"""
    return render(request, 'pages/faq.html')


def contact(request):
    """Contact page"""
    return render(request, 'pages/contact.html')


def help(request):
    """Help page"""
    return render(request, 'pages/help.html')
