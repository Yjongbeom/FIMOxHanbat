from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings

from .models import CustomUser
from .serializers import UserSerializer


def air_quality_view(request):
    context = {
        'api_key' : settings.FRONT_API_KEY,
    }

    return render(request, 'air_quality.html', context)

class AirQualityAPIView(APIView):
    def get(self, request, format=None):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        # api_key = settings.AIR_QUALITY_API_KEY
        #
        # if lat and lon:
        #     url = f'http://api.airvisual.com/v2/nearest_station?lat={lat}&lon={lon}&key={api_key}'
        #     print(url)
        #     response = requests.get(url)
        #     data = response.json()
        #
        #     return Response(data)

        api_key = settings.OPENWEATHERMAP_API_KEY

        print(lat, lon, api_key)

        if lat and lon:
            url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
            print(url)
            response = requests.get(url)
            data = response.json()

            if 'list' in data and len(data['list']) > 0:
                air_quality_data = data['list'][0]
            else:
                air_quality_data = None
        else:
            air_quality_data = None

        return Response(air_quality_data)

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class BookmarkView(APIView):
    def post(self, request):
        username = request.data.get('username')
        bookmark = request.data.get('bookmark')
        user = CustomUser.objects.filter(username=username).first()

        if user:
            user.bookmarks.append(bookmark)
            user.save()
            return Response({"message": "Bookmark added"}, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        username = request.query_params.get('username')
        user = CustomUser.objects.filter(username=username).first()

        if user:
            return Response(user.bookmarks, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
