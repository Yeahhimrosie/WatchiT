from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login),
    path('user/success', views.dashboard),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('watchd', views.watchd),
    path('watchd/<int:movie_id>', views.watchd),
    path('add_movie', views.add_movie),
    path('edit/<int:movie_id>', views.edit),
    path('save_changes/<int:movie_id>', views.save_changes),
    path('delete/<int:movie_id>', views.delete),
    path('love/<int:movie_id>', views.love),
    path('unlove/<int:movie_id>', views.unlove),
    path('watchiT_page', views.watchiT_page),
    path('watchd_page', views.watchd_page),
    path('watch_again/<int:movie_id>', views.watch_again),
    path('how_to', views.how_to),
]
