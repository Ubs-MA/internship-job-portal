from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('profile/', views.view_profile, name='view_profile'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/post/", views.post_job, name="post_job"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("jobs/<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
