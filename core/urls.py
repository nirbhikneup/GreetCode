from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('tag/<int:tag_id>/', views.questions_by_tag, name='questions_by_tag'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),

]
