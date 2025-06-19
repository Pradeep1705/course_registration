from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})

    def __str__(self):
        return f"{self.code} - {self.name}"

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')