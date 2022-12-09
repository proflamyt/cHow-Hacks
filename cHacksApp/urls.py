from django.urls import include, path
from rest_framework import routers
from .views import AnswerQuestions, Certificate, QuestionsView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionsView)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('answers/<int:pk>', AnswerQuestions.as_view(), name='answers'),
    path('certificate/', Certificate.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]