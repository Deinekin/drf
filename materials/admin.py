from django.contrib import admin

from materials.models import Course, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name", "description", "owner")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_filter = ("course", "user")
