from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)

    def __str__(self):
        return self.username

    def is_student(self):
        return self.roles.filter(name='Student').exists()

    def is_teacher(self):
        return self.roles.filter(name='Teacher').exists()


class Status(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='statuses')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status by {self.user.get_full_name()} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_courses')
    students = models.ManyToManyField(CustomUser, related_name='student_courses', blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            original = Course.objects.get(pk=self.pk)
            if original.files != self.files:
                for student in self.students.all():
                    Notification.objects.create(
                        user=student,
                        text=f"A new file has been added to the course '{self.name}'."
                    )
        super().save(*args, **kwargs)


class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_feedbacks')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.get_full_name()} on {self.course.name}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
