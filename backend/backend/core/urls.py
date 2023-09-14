from django.urls import path
from . import views

urlpatterns = [
    path(
        "schedule/create",
        views.CreateScheduleRequestAPIView.as_view(),
        name="schedule-create",
    ),
    path(
        "schedule/<int:id>",
        views.RetrieveScheduleRequestAPIView.as_view(),
        name="schedule-retrieve",
    ),
]
