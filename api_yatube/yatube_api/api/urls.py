from api.views import CommentViewSet, GroupViewSet, PostViewSet
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# v1/
router.register(r'v1/posts', PostViewSet)
router.register(r'v1/groups', GroupViewSet)
router.register(r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/api-token-auth/', obtain_auth_token),
    path('', include(router.urls))
]
