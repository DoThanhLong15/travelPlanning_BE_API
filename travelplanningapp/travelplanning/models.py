import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    rating = models.FloatField(default=0)
    ratingCount = models.IntegerField(default=0)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class TripPlan(BaseModel):
    title = models.CharField(max_length=100)
    description = RichTextField()
    startLocation = models.CharField(max_length=100, null=False)
    startTime = models.DateTimeField(null=False)
    endTime = models.DateTimeField(null=False)
    expectCost = models.FloatField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Trip(models.Model):
    destination = models.CharField(null=False, max_length=100)
    travelTime = models.TimeField(null=False)
    description = RichTextField()
    image = CloudinaryField(null=True)

    tripplan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tripplan', 'destination')


class RelateUserTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tripplan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(BaseModel, RelateUserTrip):
    content = models.TextField(max_length=255)


class UserJoinTripPlan(RelateUserTrip):

    class Meta:
        unique_together = ('tripplan', 'user')


class ReportUser(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')