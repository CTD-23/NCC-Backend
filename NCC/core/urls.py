from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'leaderboard', LeaderBoardViewSet)
router.register(r'submit', Submit,basename='submit')
router.register(r'submissions', GetSubmissions,basename='submissions')


# Only for Admin User
secretRouter = routers.DefaultRouter()
secretRouter.register(r'register',RegisterApi)
secretRouter.register(r'teamregister',TeamRegisterApi)

urlpatterns = [
    path('home/', home,name="home"),
    path('api/', include(router.urls)),
    path('secret/api/', include(secretRouter.urls)),
    path('api/login/', LoginApi.as_view(),name="login"),
]
