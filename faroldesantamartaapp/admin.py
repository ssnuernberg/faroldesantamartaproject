from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Status, Course, Feedback, Notification, Message

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'location', 'birth_date', 'roles')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'location', 'birth_date', 'roles')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Status)
admin.site.register(Course)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Message)
