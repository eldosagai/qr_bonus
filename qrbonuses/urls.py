from django.contrib import admin
from django.urls import path, include
from user import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]