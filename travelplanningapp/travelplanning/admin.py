from django.contrib import admin
from travelplanning.models import User, TripPlan, Trip, Comment,ReportUser, UserJoinTripPlan
from django.utils.html import mark_safe
from django import forms
import cloudinary


admin.site.register(User)
admin.site.register(TripPlan)
admin.site.register(Trip)
admin.site.register(Comment)
admin.site.register(ReportUser)
admin.site.register(UserJoinTripPlan)