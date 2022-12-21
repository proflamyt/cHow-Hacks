from django.urls import include, path
from rest_framework import routers
from .views import AnswerQuestions, Certificate, QuestionsView, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionsView)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('answers/<slug:school>/<int:pk>', AnswerQuestions.as_view(), name='answers'),
    path('certificate/', Certificate.as_view()),
    path('api/login', TokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('api/refresh', TokenRefreshView.as_view() , name='token_refresh')

]