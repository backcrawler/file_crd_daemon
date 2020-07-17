from django.urls import path

from . import views

app_name = 'saver'

urlpatterns = [
    path('', views.FileView.as_view()),  # POST
    path('<str:hash_name>/', views.FileView.as_view()),    # GET/DELETE
]
