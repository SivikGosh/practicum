from django.urls import path

from .views import CreateUserView, GetAPIToken

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('token/', GetAPIToken.as_view(), name='token'),
]
