from django.urls import path
from .views import PollList, PollDetail, ChoiceCreate, VoteCreate,MyTokenObtainPairView

urlpatterns = [
    path('polls/', PollList.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetail.as_view(), name='poll-detail'),
    path('choices/', ChoiceCreate.as_view(), name='choice-create'),
    path('vote/', VoteCreate.as_view(), name='vote-create'),
    path('login/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
