from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('company', 'Company')])
    university = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class JobPosting(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=[('internship', 'Internship'), ('job', 'Job')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'job')