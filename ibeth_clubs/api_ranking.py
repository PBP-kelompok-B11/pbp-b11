from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ClubRanking
from .serializers import ClubRankingSerializer

class RankingListAPI(APIView):
    def get(self, request):
        rankings = ClubRanking.objects.all().order_by('peringkat')
        serializer = ClubRankingSerializer(rankings, many=True)
        return Response(serializer.data)


class RankingDetailAPI(APIView):
    def get(self, request, pk):
        try:
            ranking = ClubRanking.objects.get(pk=pk)
        except ClubRanking.DoesNotExist:
            return Response({"error": "Ranking not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClubRankingSerializer(ranking)
        return Response(serializer.data)
