from rest_framework import serializers
from travelplanning.models import User, TripPlan, Trip, Comment, ReportUser, UserJoinTripPlan


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.avatar:
            rep['avatar'] = instance.avatar.url

        return rep

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar']


class UserDetailSerializer(UserSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ['username', 'password', 'email', 'rating', 'ratingCount']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class TripPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TripPlan
        fields = ['id', 'title', 'user']


class TripPlanDetailSerializer(TripPlanSerializer):
    class Meta:
        model = TripPlanSerializer.Meta.model
        fields = TripPlanSerializer.Meta.fields + ['description', 'startLocation', 'startTime', 'endTime', 'expectCost', 'created_date']



class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'destination', 'travelTime', 'description', 'image']


class ReportUserSerializer(serializers.ModelSerializer):
    reporter = UserSerializer()
    reported_user = UserSerializer()

    class Meta:
        model = ReportUser
        fields = ['id', 'title', 'description', 'reporter', 'reported_user']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']


class UserJoinTripPlanSerializer(serializers.ModelSerializer):
    tripplan = TripPlanSerializer()

    class Meta:
        model = UserJoinTripPlan
        fields = ['id', 'tripplan']


class AddUserJoinTripPlanSerializer(UserJoinTripPlanSerializer):
    user = UserSerializer()

    class Meta:
        model = UserJoinTripPlanSerializer.Meta.model
        fields = UserJoinTripPlanSerializer.Meta.fields + ['user']