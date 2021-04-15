from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login),
    path('user/success', views.dashboard),
    path('logout', views.logout),
    path('watchd', views.watchd),
    path('add_movie', views.add_movie),
    path('edit/<movie_id>', views.edit),
    path('delete', views.delete),
    path('love/<int:movie_id>', views.love),
    path('unlove/<int:movie_id>', views.unlove),
]
