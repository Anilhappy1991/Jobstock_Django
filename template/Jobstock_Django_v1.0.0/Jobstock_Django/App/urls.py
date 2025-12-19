from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path("", views.index, name="index"),
    path("home-2/", views.home_2, name="home_2"),
    path("home-3/", views.home_3, name="home_3"),
    path("home-4/", views.home_4, name="home_4"),
    path("home-5/", views.home_5, name="home_5"),
    path("home-6/", views.home_6, name="home_6"),
    path("home-7/", views.home_7, name="home_7"),
    path("home-8/", views.home_8, name="home_8"),
    path("home-9/", views.home_9, name="home_9"),
    path("home-10/", views.home_10, name="home_10"),
    path("home-11/", views.home_11, name="home_11"),
    path("home-12/", views.home_12, name="home_12"),
    
    path("grid-style-1/", views.grid_style_1, name="grid_style_1"),
    path("grid-style-2/", views.grid_style_2, name="grid_style_2"),
    path("grid-style-3/", views.grid_style_3, name="grid_style_3"),
    path("grid-style-4/", views.grid_style_4, name="grid_style_4"),
    path("grid-style-5/", views.grid_style_5, name="grid_style_5"),
    path("full-job-grid-1/", views.full_job_grid_1, name="full_job_grid_1"),
    path("full-job-grid-2/", views.full_job_grid_2, name="full_job_grid_2"),
    path("list-style-1/", views.list_style_1, name="list_style_1"),
    path("list-style-2/", views.list_style_2, name="list_style_2"),
    path("list-style-3/", views.list_style_3, name="list_style_3"),
    path("full-job-list-1/", views.full_job_list_1, name="full_job_list_1"),
    path("full-job-list-2/", views.full_job_list_2, name="full_job_list_2"),
    
    path("half-map/", views.half_map, name="half_map"),
    path("half-map-2/", views.half_map_2, name="half_map_2"),
    path("half-map-3/", views.half_map_3, name="half_map_3"),
    path("half-map-list-1/", views.half_map_list_1, name="half_map_list_1"),
    path("half-map-list-2/", views.half_map_list_2, name="half_map_list_2"),
    
    path("candidate-grid-1/", views.candidate_grid_1, name="candidate_grid_1"),
    path("candidate-grid-2/", views.candidate_grid_2, name="candidate_grid_2"),
    path("candidate-list-1/", views.candidate_list_1, name="candidate_list_1"),
    path("candidate-list-2/", views.candidate_list_2, name="candidate_list_2"),
    path("candidate-half-map/", views.candidate_half_map, name="candidate_half_map"),
    path("candidate-half-map-list/", views.candidate_half_map_list, name="candidate_half_map_list"),
    
    path("single-layout-1/", views.single_layout_1, name="single_layout_1"),
    path("single-layout-2/", views.single_layout_2, name="single_layout_2"),
    path("single-layout-3/", views.single_layout_3, name="single_layout_3"),
    path("single-layout-4/", views.single_layout_4, name="single_layout_4"),
    path("single-layout-5/", views.single_layout_5, name="single_layout_5"),
    path("single-layout-6/", views.single_layout_6, name="single_layout_6"),
    
    path("candidate-detail/", views.candidate_list_or_default, name="candidate_list_or_default"),
    path("candidate-detail/<slug:title>/", views.candidate_detail, name="candidate_detail"),
    
    path("candidate-detail-2/", views.candidate_detail_2, name="candidate_detail_2"),
    path("candidate-detail-3/", views.candidate_detail_3, name="candidate_detail_3"),
    
    path("advance-search/", views.advance_search, name="advance_search"),
    
    path("candidate-dashboard/", views.candidate_dashboard, name="candidate_dashboard"),
    path("candidate-profile/", views.candidate_profile, name="candidate_profile"),
    path("candidate-resume/", views.candidate_resume, name="candidate_resume"),
    path("candidate-applied-jobs/", views.candidate_applied_jobs, name="candidate_applied_jobs"),
    path("candidate-alert-job/", views.candidate_alert_job, name="candidate_alert_job"),
    path("candidate-saved-jobs/", views.candidate_saved_jobs, name="candidate_saved_jobs"),
    path("candidate-follow-employers/", views.candidate_follow_employers, name="candidate_follow_employers"),
    path("candidate-messages/", views.candidate_messages, name="candidate_messages"),
    path("candidate-change-password/", views.candidate_change_password, name="candidate_change_password"),
    path("candidate-delete-account/", views.candidate_delete_account, name="candidate_delete_account"),
    
    path("employer-grid-1/", views.employer_grid_1, name="employer_grid_1"),
    path("employer-grid-2/", views.employer_grid_2, name="employer_grid_2"),
    path("employer-list-1/", views.employer_list_1, name="employer_list_1"),
    path("employer-half-map/", views.employer_half_map, name="employer_half_map"),
    path("employer-half-map-list/", views.employer_half_map_list, name="employer_half_map_list"),
    
    path("employer-detail/", views.employer_list_or_default, name="employer_list_or_default"),
    path("employer-detail/<slug:title>/", views.employer_detail, name="employer_detail"),
    
    path("employer-detail-2/", views.employer_detail_2, name="employer_detail_2"),
    
    path("employer-dashboard/", views.employer_dashboard, name="employer_dashboard"),
    path("employer-profile/", views.employer_profile, name="employer_profile"),
    path("employer-jobs/", views.employer_jobs, name="employer_jobs"),
    path("employer-submit-job/", views.employer_submit_job, name="employer_submit_job"),
    path("employer-applicants-jobs/", views.employer_applicants_jobs, name="employer_applicants_jobs"),
    path("employer-shortlist-candidates/", views.employer_shortlist_candidates, name="employer_shortlist_candidates"),
    path("employer-package/", views.employer_package, name="employer_package"),
    path("employer-messages/", views.employer_messages, name="employer_messages"),
    path("employer-change-password/", views.employer_change_password, name="employer_change_password"),
    path("employer-delete-account/", views.employer_delete_account, name="employer_delete_account"),
    
    path("about-us/", views.about_us, name="about_us"),
    path("404/", views.notFound, name="notFound"),
    path("checkout/", views.checkout, name="checkout"),
    path("blog/", views.blog, name="blog"),
    
    path("blog-detail/", views.blog_list_or_default, name="blog_list_or_default"),
    path("blog-detail/<slug:title>/", views.blog_detail, name="blog_detail"),
    
    path("privacy/", views.privacy, name="privacy"),
    path("pricing/", views.pricing, name="pricing"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    
    path("help/", views.help, name="help"),
    
    path("job-detail/", views.job_list_or_default, name="job_list_or_default"),
    path("job-detail/<slug:title>/", views.job_detail, name="job_detail"),
    
    path("signup/", views.signup, name="signup"),
    path("slider-home/", views.slider_home, name="slider_home"),
]