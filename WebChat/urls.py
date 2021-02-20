from django.urls import path
from . import views
app_name = 'WebChat'
urlpatterns = [
    path("<int:pk>/", views.ChatView.as_view(),name='chat'),
    path('<int:pk>/create/', views.MessageCreate, name = "create")
]
