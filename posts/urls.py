from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('vote/<int:pk>', views.VoteCreate.as_view()),
    path('delete/<int:pk>', views.PostRetrive.as_view()),
]