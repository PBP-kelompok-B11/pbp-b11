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

    def post(self, request):
        serializer = ClubRankingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RankingDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return ClubRanking.objects.get(pk=pk)
        except ClubRanking.DoesNotExist:
            return None
        
    def get(self, request, pk):
        try:
            ranking = ClubRanking.objects.get(pk=pk)
        except ClubRanking.DoesNotExist:
            return Response({"error": "Ranking not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClubRankingSerializer(ranking)
        return Response(serializer.data)
    
    def put(self, request, pk):
        ranking = self.get_object(pk)
        if ranking is None:
            return Response({"error": "Ranking not found."}, status=404)

        serializer = ClubRankingSerializer(ranking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
