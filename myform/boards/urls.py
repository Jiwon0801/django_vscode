from django.urls import path
from . import views

app_name='boards'
urlpatterns = [
    path('', views.index, name="index" ),
    path('create/', views.create, name="create"),
    path('<int:board_pk>/', views.detail, name="detail"),
]
