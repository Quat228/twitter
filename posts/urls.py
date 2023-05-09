from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('tweet', views.TweetViewSet)
router.register('tweet/reply/', views.TweetReplyViewSet)

router.register('reply', views.ReplyViewSet)


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
