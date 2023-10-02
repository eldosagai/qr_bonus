from django.contrib import admin
from django.urls import path, include
from user import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
# router.register(r'register/', views.register_user, basename="register")
# router.register(r'logout', views.user_logout, basename="logout")


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    # path('register/', views.register_user, name='register'),
    # path('logout/', views.user_logout, name='logout'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('login-with-otp/', views.LoginWithOTP.as_view(), name='login-with-otp'),
    # path('validate-otp/', views.ValidateOTP.as_view(), name='validate-otp'),
]
