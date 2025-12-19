"""
Home page views - All home layout variations
"""
from django.shortcuts import render


def index(request):
    """Home layout 1"""
    return render(request, 'pages/index.html')


def home_2(request):
    """Home layout 2"""
    return render(request, 'pages/home-2.html')


def home_3(request):
    """Home layout 3"""
    return render(request, 'pages/home-3.html')


def home_4(request):
    """Home layout 4"""
    return render(request, 'pages/home-4.html')


def home_5(request):
    """Home layout 5"""
    return render(request, 'pages/home-5.html')


def home_6(request):
    """Home layout 6"""
    return render(request, 'pages/home-6.html')


def home_7(request):
    """Home layout 7"""
    return render(request, 'pages/home-7.html')


def home_8(request):
    """Home layout 8"""
    return render(request, 'pages/home-8.html')


def home_9(request):
    """Home layout 9"""
    return render(request, 'pages/home-9.html')


def home_10(request):
    """Home layout 10"""
    return render(request, 'pages/home-10.html')


def home_11(request):
    """Home layout 11"""
    return render(request, 'pages/home-11.html')


def home_12(request):
    """Home layout 12"""
    return render(request, 'pages/home-12.html')


def slider_home(request):
    """Slider home page"""
    return render(request, 'pages/slider-home.html')
