from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, View
from .models import CustomUser, Role, Status, Course, Feedback, Notification, Message
from .forms import CustomUserChangeForm, CustomUserCreationForm, StatusForm, CourseForm, FeedbackForm
from rest_framework import viewsets, permissions
from .serializers import RoleSerializer, CustomUserSerializer, StatusSerializer, CourseSerializer, FeedbackSerializer, NotificationSerializer
import json

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False) if request.user.is_authenticated else None
    return render(request, 'index.html', {'notifications': notifications})

def about(request):
    return render(request, 'about.html')

def events(request):
    # This would typically come from your database
    upcoming_events = [
        {
            'title': 'Beach Clean-Up at Praia do Cardoso',
            'date': '2024-08-15',
            'location': 'Praia do Cardoso, Farol de Santa Marta',
            'description': 'Join us for a beach clean-up event to help keep our shores clean and beautiful.',
        },
        {
            'title': 'Educational Workshop on Marine Conservation',
            'date': '2024-09-10',
            'location': 'Community Center, Farol de Santa Marta',
            'description': 'A workshop to educate the community about the importance of marine conservation.',
        },
        # Add more events as needed
    ]
    return render(request, 'events.html', {'upcoming_events': upcoming_events})


def get_involved(request):
    return render(request, 'get_involved.html')

def donate(request):
    return render(request, 'donate.html')

def store(request):
    # This would typically come from your database
    products = [
        {
            'name': 'Eco-friendly Water Bottle',
            'price': 'R$119',
            'description': 'Reusable water bottle made from sustainable materials.',
            'image_url': 'path_to_image.jpg',
        },
        {
            'name': 'Reusable Tote Bag',
            'price': 'R$49',
            'description': 'Stylish tote bag perfect for carrying groceries or beach gear.',
            'image_url': 'path_to_image.jpg',
        },
        # Add more products as needed
    ]
    return render(request, 'store.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})


@login_required
def profile_change(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('faroldesantamartaapp:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/profile_change_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign the "Student" role to the user
            student_role = Role.objects.get(name='Student')
            user.roles.add(student_role)
            user.save()

            login(request, user)
            return redirect('faroldesantamartaapp:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher()


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'user_list.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user_detail'
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = StatusForm()
        context['statuses'] = self.object.statuses.all()
        return context


class UserCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('faroldesantamartaapp:user_list')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_form.html'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:user_detail', kwargs={'pk': self.object.pk})


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('faroldesantamartaapp:user_list')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'status_list.html'

    def get_queryset(self):
        return Status.objects.all().order_by('-created_at')

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically set the user to the current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:user_detail', kwargs={'pk': self.object.user.pk})


class StatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_form.html'

    def test_func(self):
        status = self.get_object()
        return self.request.user == status.user  # Only allow the user who created the status to edit it

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:user_detail', kwargs={'pk': self.object.user.pk})


class StatusDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Status
    template_name = 'status_confirm_delete.html'

    def test_func(self):
        status = self.get_object()
        return self.request.user == status.user  # Only allow the user who created the status to delete it

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:user_detail', kwargs={'pk': self.object.user.pk})


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course_list.html'


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_form'] = FeedbackForm()
        context['feedbacks'] = self.object.feedbacks.all()
        return context


class CourseCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('faroldesantamartaapp:course_list')


class CourseUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('faroldesantamartaapp:course_list')


class CourseDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Course
    context_object_name = 'course'
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('faroldesantamartaapp:course_list')


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course = Course.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:course_detail', kwargs={'pk': self.object.course.pk})


class FeedbackUpdateView(UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        return context

    def get_queryset(self):
        return Feedback.objects.all().order_by('-created_at')

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:course_detail', kwargs={'pk': self.object.course.pk})


class FeedbackDeleteView(DeleteView):
    model = Feedback
    template_name = 'feedback_confirm_delete.html'
    success_url = reverse_lazy('faroldesantamartaapp:feedback_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        return context

    def get_success_url(self):
        return reverse_lazy('faroldesantamartaapp:course_detail', kwargs={'pk': self.object.course.pk})


class CourseEnrollView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('faroldesantamartaapp:course_detail', kwargs={'pk': self.kwargs.get('course_id')})

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        course.students.add(request.user)
        Notification.objects.create(
            user=course.teacher,
            text=f"{request.user.get_full_name()} has enrolled in your course '{course.name}'."
        )
        messages.success(request, "You've successfully enrolled in the course.")
        return super().post(request, *args, **kwargs)


class CourseUnenrollView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        self.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return self.request.user == self.course.teacher

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(CustomUser, id=kwargs['student_id'])
        self.course.students.remove(student)
        messages.success(request, f'Student {student.get_full_name()} has been unenrolled from {self.course.name}.')
        return redirect('faroldesantamartaapp:course_detail', pk=self.course.id)


@login_required
def notification_mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('faroldesantamartaapp:index')


@login_required
def chat(request, room_name):
    return render(request, 'chat_room.html', {'room_name': room_name})


@login_required
def chat_post_message(request, room_name):
    data = json.loads(request.body)
    text = data.get('text')
    user = request.user
    Message.objects.create(user=user, text=text)
    return JsonResponse({"success": True})


@login_required
def chat_get_messages(request, room_name):
    messages = Message.objects.all().order_by('created_at').values('user__username', 'text', 'created_at')[:50]
    return JsonResponse(list(messages), safe=False)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def chat_clear_room(request, room_name):
    Message.objects.all().delete()  # Delete all messages
    return redirect('faroldesantamartaapp:chat', room_name='faroldesantamarta')
