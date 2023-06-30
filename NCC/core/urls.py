from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'leaderboard', LeaderBoardViewSet)
router.register(r'submit', Submit,basename='submit')
router.register(r'submissions', GetSubmissions,basename='submissions')

urlpatterns = [
    # path('home/', home,name="home"),
    path('api/', include(router.urls)),
]
