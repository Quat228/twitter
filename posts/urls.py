from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('tweet', views.TweetViewSet)
router.register('reply', views.ReplyViewSet)

urlpatterns = [
    path('viewset/', include(router.urls))
]
