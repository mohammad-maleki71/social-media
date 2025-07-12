from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('details/<int:post_id>/', views.PostDetailsView.as_view(), name='details'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='update'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnFollowView.as_view(), name='unfollow'),
]