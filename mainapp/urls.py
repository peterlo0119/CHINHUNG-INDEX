from django.urls import path
from . import views
from .views import frontend_update_group

urlpatterns = [
    path('', views.index, name='index'),
    path('stream/<str:group>/', views.stream, name='stream'),
    path('anime/', views.anime, name='anime'),
    path('manga/', views.manga, name='manga'),
    path('novel/', views.novel, name='novel'),
    path("update_group/<str:group>/", frontend_update_group, name="frontend_update_group"),
    path("anime/update", views.frontend_update_anime, name="update_anime"),
    path("manga/", mainapp.views.manga, name="manga"),
]