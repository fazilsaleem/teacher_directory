"""
teacher app  URL Configurations.
"""

from django.urls import path
from administration.views import DashboradView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    path('', DashboradView.as_view(), name = 'dashboard'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('user-profile/<int:pk>', UserProfileView.as_view(), name = 'user-profile'),
]
