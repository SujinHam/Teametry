# teamapp/urls.py

from django.urls import path
from .views import (
    TeamCreateView,
    RoomJoinView,
    ParticipantJoinView,
    SurveySubmitView,
    TeamAssignView,
    SurveyStatusView,
    TeamResultView,
    TeamDetailView,
    ParticipantSummaryView,
)

urlpatterns = [
    path('create-team/', TeamCreateView.as_view(), name='create-team'),
    path('join-room/', RoomJoinView.as_view(), name='join-room'),
    path('join-participant/', ParticipantJoinView.as_view(), name='join-participant'),
    path('submit-survey/', SurveySubmitView.as_view(), name='submit-survey'),
    path('assign-team/', TeamAssignView.as_view(), name='assign-team'),
    path('survey-status/', SurveyStatusView.as_view(), name='survey-status'),
    path('team-result/', TeamResultView.as_view(), name='team-result'),
    path('team-detail/<str:room_code>/<int:team_number>/', TeamDetailView.as_view(), name='team-detail'),
    path('participant-summary/<int:participant_id>/', ParticipantSummaryView.as_view(), name='participant-summary'),
]
