from django.urls import path
from . import views

urlpatterns = [
    path('',views.lawyer,name = "lawyer"),
    path('pastcase/',views.pastcase.as_view(), name = "resolved cases"),
    path('resolved/',views.keyword.as_view(), name = "keyword")
]

