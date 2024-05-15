import datetime

from django.db.models import Q
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from travelplanning.models import User, TripPlan, Trip, Comment, ReportUser, UserJoinTripPlan
from travelplanning import serializers, paginators, utils, dao
from travelplanning.permiss import ItemOwner


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserDetailSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user', 'joined_trippplan']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserDetailSerializer(user).data)

    @action(methods=['get'], url_path='joined-tripplan', detail=False)
    def joined_trippplan(self, request):
        tripplan = request.user.userjointripplan_set.all()

        return Response(serializers.UserJoinTripPlanSerializer(tripplan, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='tripplan', detail=True)
    def add_tripplan(self, request, pk):
        tripplan = self.get_object().tripplan_set.create(title=request.data.get('title'),
                                                         description=request.data.get('description'),
                                                         startLocation=request.data.get('startLocation'),
                                                         startTime=request.data.get('startTime'),
                                                         endTime=request.data.get('endTime'),
                                                         expectCost=request.data.get('expectCost'))

        return Response(serializers.TripPlanSerializer(tripplan).data, status=status.HTTP_201_CREATED)


class TripPlanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TripPlan.objects.all().select_related('user')
    serializer_class = serializers.TripPlanDetailSerializer
    pagination_class = paginators.ItemPaginator

    def get_queryset(self):
        queryset = self.queryset.filter(startTime__gt=datetime.datetime.now())

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(Q(title__icontains=q) | Q(startLocation__icontains=q) |\
                                           Q(trip__destination__icontains=q))\

        return queryset

    def get_permissions(self):
        if self.action in ['add_comment', 'add_trip']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='trips', detail=True)
    def get_trip(self, request, pk):
        trip = self.get_object().trip_set.all()

        return Response(serializers.TripSerializer(trip, many=True).data,status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='trip', detail=True)
    def add_trip(self, request, pk):
        tripplan = self.get_object()
        if ItemOwner.has_object_permission(self, request, {}, tripplan):
            try:
                trip = tripplan.trip_set.create(destination=request.data.get("destination"),
                                                         travelTime=request.data.get("travelTime"),
                                                         description=request.data.get("description"),
                                                         image=request.data.get("image"))

                return Response(serializers.TripSerializer(trip).data, status=status.HTTP_201_CREATED)
            except:
                return utils.UniqueTogetherExcept(request.data.get("destination"))

        return utils.ResponseBadRequest()

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').all()

        pagina = paginators.CommentPaginator()
        page = pagina.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)

            return pagina.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comment', detail=True)
    def add_comment(self, request, pk):
        c = self.get_object().comment_set.create(user=request.user, content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=['delete'], url_path='delete', detail=True)
    def delete_tripplan(self, request, pk):
        if ItemOwner.has_object_permission(self, request, {}, self.get_object()):
            trip = self.get_object().trip_set.all()
            trip.delete()

            tripplan = self.get_object()
            tripplan.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return utils.ResponseBadRequest()

    @action(methods=['patch'], url_path='update', detail=True)
    def patch_tripplan(self, request, pk):
        tripplan = self.get_object()
        if ItemOwner.has_object_permission(self, request, {}, tripplan):
            for k, v in request.data.items():
                setattr(tripplan, k, v)
            tripplan.save()

            return Response(serializers.TripPlanDetailSerializer(tripplan).data, status=status.HTTP_200_OK)

        return utils.ResponseBadRequest()

    @action(methods=['post'], url_path='user-join', detail=True)
    def user_join_tripplan(self, request, pk):
        tripplan = self.get_object()

        if ItemOwner.has_object_permission(self, request, {}, tripplan):
            user_join = dao.get_user_by_id(id=request.data.get('user_id'))

            if user_join.id != request.user.id:
                user_join_tripplan = self.get_object().userjointripplan_set.create(
                    user=user_join)

                return Response(serializers.AddUserJoinTripPlanSerializer(user_join_tripplan).data,
                                status=status.HTTP_201_CREATED)

        return utils.ResponseBadRequest()

class TripViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Trip.objects
    serializer_class = serializers.TripSerializer

    @action(methods=['delete'], url_path='delete', detail=True)
    def delete_trip(self, request, pk):
        trip = self.get_object()
        tripplan = TripPlan.objects.get(pk=trip.tripplan_id)

        if ItemOwner.has_object_permission(self, request, {}, tripplan):
            trip.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return utils.ResponseBadRequest()

    @action(methods=['patch'], url_path='update', detail=True)
    def patch_trip(self, request, pk):
        trip = self.get_object()
        tripplan = TripPlan.objects.get(pk=trip.tripplan_id)

        if ItemOwner.has_object_permission(self, request, {}, tripplan):
            for k, v in request.data.items():
                setattr(trip, k, v)
            trip.save()

            return Response(serializers.TripSerializer(trip).data, status=status.HTTP_200_OK)

        return utils.ResponseBadRequest()


class ReportUserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ReportUser.objects.select_related('reporter').select_related('reported_user')
    serializer_class = serializers.ReportUserSerializer
    permission_classes = [permissions.IsAdminUser,]

    @action(methods=['post'], url_path='create', detail=False)
    def create_report(self, request):
        if permissions.IsAuthenticated:
            report = ReportUser(title=request.data.get("title"),
                                description=request.data.get("description"),
                                reporter=User.objects.get(pk=request.data.get("reporter")),
                                reported_user=User.objects.get(pk=request.data.get("reported_user"))
            )
            report.save()

            return Response(serializers.ReportUserSerializer(report).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [ItemOwner]