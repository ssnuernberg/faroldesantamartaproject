from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Course, Status, Feedback, Notification
from django.contrib.auth.models import AnonymousUser
from .forms import CustomUserChangeForm, CustomUserCreationForm, StatusForm, CourseForm, FeedbackForm

# Utility function for creating a user
def create_user(username, password, is_teacher=False):
    user = CustomUser.objects.create_user(username=username, password=password)
    if is_teacher:
        # Assuming you have a method to set a user as a teacher
        user.set_as_teacher()  # You might need to adjust this according to your model methods
    user.save()
    return user

# Tests for index view
class IndexViewTests(TestCase):
    def test_no_login_redirect(self):
        """
        Test that the index view redirects to login page if the user is not logged in.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_access_with_login(self):
        """
        Test that the index page is accessible when the user is logged in.
        """
        user = create_user('testuser', '12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_access(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_context_without_login(self):
        response = self.client.get(reverse('index'))
        self.assertIsNone(response.context['notifications'])

    def test_context_with_login(self):
        # Assuming the setup for a user and notifications exists
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertIsNotNone(response.context['notifications'])
        # Further assertions can be made based on the setup

class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.test_user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.test_user.save()

    def test_redirect_if_not_logged_in(self):
        # Access the profile view without being logged in
        response = self.client.get(reverse('faroldesantamartaapp:profile'))
        # Check if the response redirects to the login page
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

    def test_logged_in_uses_correct_template(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        # Access the profile view
        response = self.client.get(reverse('faroldesantamartaapp:profile'))

        # Check for the status code 200 OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'registration/profile.html')

    def test_profile_contains_user_info(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        # Access the profile view
        response = self.client.get(reverse('faroldesantamartaapp:profile'))

        # Check if the context contains the user's information
        self.assertEqual(str(response.context['user']), 'testuser')
