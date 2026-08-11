from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    """Student profile linked to Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='students/profiles/', null=True, blank=True)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name() or self.user.username}"


class Course(models.Model):
    """Academic course."""
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField(default=3)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    instructor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_teaching'
    )
    max_students = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='enrolled').count()


class Enrollment(models.Model):
    """Student enrollment in a course."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student} → {self.course} ({self.status})"


class Assignment(models.Model):
    """Assignment belonging to a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.course.code}: {self.title}"


class Submission(models.Model):
    """Student submission for an assignment."""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    feedback = models.TextField(blank=True)
    is_late = models.BooleanField(default=False)

    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
