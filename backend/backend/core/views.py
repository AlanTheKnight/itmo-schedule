from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .tasks import process_schedule_request
from .models import ScheduleRequest


class ScheduleSerializer(serializers.Serializer):
    """Serializer for the schedule view."""

    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    date_start = serializers.DateField()
    date_end = serializers.DateField()


class ScheduleRequestSerializer(serializers.ModelSerializer):
    """Serializer for the schedule request model."""

    class Meta:
        model = ScheduleRequest
        fields = "__all__"


class CreateScheduleRequestAPIView(APIView):
    """View for creating a schedule request.

    This view will create a schedule request and return it.
    """

    @method_decorator(cache_page(60 * 60 * 0.5))  # Cache for 30 minutes
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            req = ScheduleRequest.objects.create(
                status="status.Queued",
                ics_file=None,
                error=None,
            )
            process_schedule_request.delay(req.id, serializer.validated_data)
            response = ScheduleRequestSerializer(req)
            return Response(response.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class RetrieveScheduleRequestAPIView(RetrieveAPIView):
    """View for retrieving a schedule request."""

    queryset = ScheduleRequest.objects.all()
    serializer_class = ScheduleRequestSerializer
    lookup_field = "id"
