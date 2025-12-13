from rest_framework import generics
from .models import Club
from .serializers import ClubSerializer

class ClubListAPI(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class ClubDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
