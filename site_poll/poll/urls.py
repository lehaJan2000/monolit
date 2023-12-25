from django.urls import path
from . import views
from .views import BBLoginView, RegisterView, profile, delete_profile, delete_poll

urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<int:id>', profile, name='profile'),
    path('login/', BBLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create/', views.create, name='create'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('results/<poll_id>/', views.results, name='results'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('delete_poll/', delete_poll, name='delete_poll'),



]

