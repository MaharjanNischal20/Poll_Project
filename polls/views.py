from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, UserSerializerWithToken, VoteSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PollList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            poll = Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PollSerializer(poll, context={'request': request})
        return Response(serializer.data)


class ChoiceCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        choice_id = request.data.get('choice')
        if not choice_id:
            return Response({"error": "Choice ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            choice = Choice.objects.get(id=choice_id)
        except Choice.DoesNotExist:
            return Response({"error": "Choice not found or does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with vote creation logic
        if Vote.objects.filter(user=user, choice__poll=choice.poll).exists():
            return Response({"detail": "You have already voted in this poll."},
                            status=status.HTTP_400_BAD_REQUEST)

        vote = Vote(user=user, choice=choice)
        vote.save()

        vote_serializer = VoteSerializer(vote)
        return Response(vote_serializer.data, status=status.HTTP_201_CREATED)
