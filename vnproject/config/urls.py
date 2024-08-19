"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vnproject.views import air_quality_view, AirQualityAPIView, RegisterUserView, LoginView, BookmarkView

urlpatterns = [
    path('', air_quality_view, name='air_quality'),  # HTML 페이지 렌더링
    path('api/air-quality/', AirQualityAPIView.as_view(), name='air_quality_api'),  # JSON 데이터 제공
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('bookmarks/', BookmarkView.as_view(), name='bookmarks'),
]