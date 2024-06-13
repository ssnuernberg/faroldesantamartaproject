
from django.test import TestCase
from faroldesantamartaapp.models import CustomUser, Status, Role, Course, Feedback, Notification, Message

class RoleModelTests(TestCase):

    def test_role_creation(self):
        role = Role.objects.create(name='Student')
        self.assertTrue(isinstance(role, Role))
        self.assertEqual(role.__str__(), role.name)

    def test_role_update(self):
        role = Role.objects.create(name='Student')
        role.name = 'Teacher'
        role.save()
        self.assertEqual(role.name, 'Teacher')

    def test_role_deletion(self):
        role = Role.objects.create(name='Student')
        role_id = role.id
        role.delete()
        with self.assertRaises(Role.DoesNotExist):
            Role.objects.get(id=role_id)

class CustomUserModelTests(TestCase):

    def test_custom_user_creation(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(user.__str__(), user.username)

    def test_custom_user_update(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        user.email = 'newtest@example.com'
        user.save()
        self.assertEqual(user.email, 'newtest@example.com')

    def test_custom_user_deletion(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        user_id = user.id
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

class StatusModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_status_creation(self):
        status = Status.objects.create(user=self.user, text='Test status')
        self.assertTrue(isinstance(status, Status))
        self.assertEqual(status.__str__(), f"Status by {status.user.get_full_name()} on {status.created_at.strftime('%Y-%m-%d %H:%M')}")

    def test_status_update(self):
        status = Status.objects.create(user=self.user, text='Test status')
        status.text = 'Updated status'
        status.save()
        self.assertEqual(status.text, 'Updated status')

    def test_status_deletion(self):
        status = Status.objects.create(user=self.user, text='Test status')
        status_id = status.id
        status.delete()
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=status_id)

class CourseModelTests(TestCase):

    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher', email='teacher@example.com', password='testpass', is_staff=True)

    def test_course_creation(self):
        course = Course.objects.create(name='Test Course', description='Test Description', teacher=self.teacher)
        self.assertTrue(isinstance(course, Course))
        self.assertEqual(course.__str__(), course.name)

    def test_course_update(self):
        course = Course.objects.create(name='Test Course', description='Test Description', teacher=self.teacher)
        course.name = 'Updated Course'
        course.save()
        self.assertEqual(course.name, 'Updated Course')

    def test_course_deletion(self):
        course = Course.objects.create(name='Test Course', description='Test Description', teacher=self.teacher)
        course_id = course.id
        course.delete()
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)

class FeedbackModelTests(TestCase):

    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher', email='teacher@example.com', password='testpass', is_staff=True)
        self.student = CustomUser.objects.create_user(username='student', email='student@example.com', password='testpass')
        self.course = Course.objects.create(name='Test Course', description='Test Description', teacher=self.teacher)

    def test_feedback_creation(self):
        feedback = Feedback.objects.create(course=self.course, user=self.student, text='Test feedback')
        self.assertTrue(isinstance(feedback, Feedback))
        self.assertEqual(feedback.__str__(), f"Feedback by {feedback.user.get_full_name()} on {feedback.course.name}")

    def test_feedback_update(self):
        feedback = Feedback.objects.create(course=self.course, user=self.student, text='Test feedback')
        feedback.text = 'Updated feedback'
        feedback.save()
        self.assertEqual(feedback.text, 'Updated feedback')

    def test_feedback_deletion(self):
        feedback = Feedback.objects.create(course=self.course, user=self.student, text='Testfeedback')
        feedback_id = feedback.id
        feedback.delete()
        with self.assertRaises(Feedback.DoesNotExist):
            Feedback.objects.get(id=feedback_id)

class NotificationModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_notification_creation(self):
        notification = Notification.objects.create(user=self.user, text='Test notification')
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(notification.__str__(), f"Notification for {notification.user.username} - {'Read' if notification.is_read else 'Unread'}")

    def test_notification_mark_as_read(self):
        notification = Notification.objects.create(user=self.user, text='Test notification', is_read=False)
        notification.is_read = True
        notification.save()
        self.assertTrue(notification.is_read)

    def test_notification_deletion(self):
        notification = Notification.objects.create(user=self.user, text='Test notification')
        notification_id = notification.id
        notification.delete()
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notification_id)

class MessageModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_message_creation(self):
        message = Message.objects.create(user=self.user, text='Test message')
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.__str__(), f"Message by {message.user.username} on {message.created_at.strftime('%Y-%m-%d %H:%M')}")

    def test_message_deletion(self):
        message = Message.objects.create(user=self.user, text='Test message')
        message_id = message.id
        message.delete()
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message_id)
