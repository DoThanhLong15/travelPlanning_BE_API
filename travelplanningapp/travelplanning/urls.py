from django.urls import path, include
from rest_framework import routers
from travelplanning import views

r = routers.DefaultRouter()
r.register('users', views.UserViewSet, 'users')
r.register('tripplans', views.TripPlanViewSet, 'tripplans')
r.register('trips', views.TripViewSet, 'trips')
r.register('report-user', views.ReportUserViewSet, 'report-user')
r.register('comments', views.CommentViewSet, 'comments')


urlpatterns = [
    path('', include(r.urls))
]