from django.contrib import admin
from .models import Student, Course, Enrollment, Assignment, Submission


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'enrollment_date', 'is_active']
    list_filter = ['is_active', 'enrollment_date']
    search_fields = ['student_id', 'user__username', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'level', 'credits', 'instructor', 'enrolled_count', 'is_active']
    list_filter = ['level', 'is_active', 'credits']
    search_fields = ['code', 'title', 'description']
    raw_id_fields = ['instructor']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'grade', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student__student_id', 'course__code', 'course__title']
    raw_id_fields = ['student', 'course']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'max_score']
    list_filter = ['due_date', 'course']
    search_fields = ['title', 'course__code']
    raw_id_fields = ['course']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'score', 'is_late']
    list_filter = ['is_late', 'submitted_at']
    search_fields = ['student__student_id', 'assignment__title']
    raw_id_fields = ['assignment', 'student']
