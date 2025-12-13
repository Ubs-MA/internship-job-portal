from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile, JobPosting, Application

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid() and role in ['student', 'company']:
            user = form.save()
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def job_list(request):
    jobs = JobPosting.objects.all().order_by('-created_at')
    return render(request, 'jobs/list.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.user.profile.role != 'company':
        return redirect('home')

    if request.method == 'POST':
        JobPosting.objects.create(
            company=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            job_type=request.POST['job_type']
        )
        return redirect('job_list')

    return render(request, 'jobs/post_job.html')

def job_detail(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    already_applied = False
    if request.user.is_authenticated and request.user.profile.role == 'student':
        already_applied = Application.objects.filter(student=request.user, job=job).exists()
    
    return render(request, 'jobs/detail.html', {
        'job': job,
        'already_applied': already_applied
    })

@login_required
def apply_job(request, job_id):
    if request.user.profile.role != 'student':
        return redirect('job_list')
    
    job = JobPosting.objects.get(id=job_id)
    
    # Prevent duplicate
    if Application.objects.filter(student=request.user, job=job).exists():
        return redirect('job_detail', job_id=job_id)
    
    Application.objects.create(student=request.user, job=job)
    return redirect('job_detail', job_id=job_id)

@login_required
def dashboard(request):
    # Safely get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if profile.role == 'student':
        applications = Application.objects.filter(student=request.user).order_by('-applied_at')
        return render(request, 'dashboard/student.html', {'applications': applications})
    elif profile.role == 'company':
        my_jobs = JobPosting.objects.filter(company=request.user).order_by('-created_at')
        return render(request, 'dashboard/company.html', {'my_jobs': my_jobs})
    else:
        # Default fallback
        return redirect('home')

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Common fields
        if 'email' in request.POST:
            profile.email = request.POST['email'] or None
        
        # Student-specific
        if profile.role == 'student':
            profile.university = request.POST['university']
            profile.skills = request.POST['skills']
            if 'cv' in request.FILES:
                profile.cv = request.FILES['cv']
        
        profile.save()
        return redirect('view_profile')
    
    return render(request, 'profile/edit.html', {'profile': profile})

@login_required
def job_applicants(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    if job.company != request.user:
        return redirect('home')
    
    applicants = Application.objects.filter(job=job)
    return render(request, 'dashboard/applicants.html', {
        'job': job,
        'applicants': applicants
    })

@login_required
def view_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile/view.html', {'profile': profile})