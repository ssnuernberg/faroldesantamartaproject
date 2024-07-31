from django.urls import path, include
from . import views

app_name = 'faroldesantamartaapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),  
    path('get_involved/', views.get_involved, name='get_involved'),  
    path('donate/', views.donate, name='donate'),     
    path('store/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile_change/', views.profile_change, name='profile_change'),
    path('accounts/register/', views.register, name='register'),

    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    path('edupdates/', views.StatusListView.as_view(), name='status_list'),
    path('edupdates/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('edupdates/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_update'),
    path('edupdates/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('courses/<int:pk>/feedbacks/create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedbacks/<int:pk>/edit/', views.FeedbackUpdateView.as_view(), name='feedback_update'),
    path('feedbacks/<int:pk>/delete/', views.FeedbackDeleteView.as_view(), name='feedback_delete'),

    path('courses/<int:course_id>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
    path('courses/<int:course_id>/unenroll/<int:student_id>/', views.CourseUnenrollView.as_view(), name='course_unenroll'),

    path('notifications/<int:notification_id>/read/', views.notification_mark_as_read, name='notification_mark_as_read'),

    path('chat/<str:room_name>/', views.chat, name='chat'),
    path('chat/<str:room_name>/post_message/', views.chat_post_message, name='chat_post_message'),
    path('chat/<str:room_name>/get_messages/', views.chat_get_messages, name='chat_get_messages'),
    path('chat/<str:room_name>/clear/', views.chat_clear_room, name='chat_clear_room'),

]
