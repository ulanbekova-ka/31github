from django.urls import path
from views import QuestionList, AnswerList
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('answers/', AnswerList.as_view(), name='answer-list'),
]


urlpatterns2 = [
    path('admin/', admin.site.urls),
    path('api/', include('yourapp.urls')),
]
