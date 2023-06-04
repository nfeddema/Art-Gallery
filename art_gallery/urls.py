from django.urls import path
from art_gallery import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<category>', views.category, name='art-category'),
    path('artpiece/<art_piece_id>', views.artPiecePage, name='art-piece'),
]