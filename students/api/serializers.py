from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student, Course, Enrollment, Assignment, Submission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_id', 'student_id', 'date_of_birth',
            'phone', 'address', 'enrollment_date', 'is_active', 'profile_picture'
        ]
        read_only_fields = ['enrollment_date']


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='instructor',
        write_only=True, allow_null=True, required=False
    )
    enrolled_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'title', 'description', 'credits', 'level',
            'instructor', 'instructor_id', 'max_students', 'is_active',
            'enrolled_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_id', 'course', 'course_id',
            'status', 'enrolled_at', 'grade', 'notes'
        ]
        read_only_fields = ['enrolled_at']


class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Assignment
        fields = [
            'id', 'course', 'course_id', 'title', 'description',
            'due_date', 'max_score', 'created_at'
        ]
        read_only_fields = ['created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    assignment_id = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all(), source='assignment', write_only=True
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )

    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'assignment_id', 'student', 'student_id',
            'submitted_at', 'content', 'file', 'score', 'feedback', 'is_late'
        ]
        read_only_fields = ['submitted_at']
