"""
Job-related views - Job listings, details, and search
"""
from django.shortcuts import render, get_object_or_404
from App.models import Job


def grid_style_1(request):
    """Job grid style 1"""
    return render(request, 'pages/grid-style-1.html')


def grid_style_2(request):
    """Job grid style 2"""
    return render(request, 'pages/grid-style-2.html')


def grid_style_3(request):
    """Job grid style 3"""
    return render(request, 'pages/grid-style-3.html')


def grid_style_4(request):
    """Job grid style 4"""
    return render(request, 'pages/grid-style-4.html')


def grid_style_5(request):
    """Job grid style 5"""
    return render(request, 'pages/grid-style-5.html')


def full_job_grid_1(request):
    """Full job grid 1"""
    return render(request, 'pages/full-job-grid-1.html')


def full_job_grid_2(request):
    """Full job grid 2"""
    return render(request, 'pages/full-job-grid-2.html')


def list_style_1(request):
    """Job list style 1"""
    return render(request, 'pages/list-style-1.html')


def list_style_2(request):
    """Job list style 2"""
    return render(request, 'pages/list-style-2.html')


def list_style_3(request):
    """Job list style 3"""
    return render(request, 'pages/list-style-3.html')


def full_job_list_1(request):
    """Full job list 1"""
    return render(request, 'pages/full-job-list-1.html')


def full_job_list_2(request):
    """Full job list 2"""
    return render(request, 'pages/full-job-list-2.html')


def half_map(request):
    """Job half map view"""
    return render(request, 'pages/half-map.html')


def half_map_2(request):
    """Job half map view 2"""
    return render(request, 'pages/half-map-2.html')


def half_map_3(request):
    """Job half map view 3"""
    return render(request, 'pages/half-map-3.html')


def half_map_list_1(request):
    """Job half map list 1"""
    return render(request, 'pages/half-map-list-1.html')


def half_map_list_2(request):
    """Job half map list 2"""
    return render(request, 'pages/half-map-list-2.html')


def single_layout_1(request):
    """Job single layout 1"""
    return render(request, 'pages/single-layout-1.html')


def single_layout_2(request):
    """Job single layout 2"""
    return render(request, 'pages/single-layout-2.html')


def single_layout_3(request):
    """Job single layout 3"""
    return render(request, 'pages/single-layout-3.html')


def single_layout_4(request):
    """Job single layout 4"""
    return render(request, 'pages/single-layout-4.html')


def single_layout_5(request):
    """Job single layout 5"""
    return render(request, 'pages/single-layout-5.html')


def single_layout_6(request):
    """Job single layout 6"""
    return render(request, 'pages/single-layout-6.html')


def advance_search(request):
    """Advanced job search"""
    return render(request, 'pages/advance-search.html')


def job_list_or_default(request):
    """Job list or default view"""
    jobs = Job.objects.all()
    return render(request, 'pages/job-detail.html', {'jobs': jobs})


def job_detail(request, title):
    """Job detail page by title/slug"""
    job = get_object_or_404(Job, slug=title)
    return render(request, 'pages/job-detail.html', {'job': job})
