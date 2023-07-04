from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name = "home"),
   path('about/',views.about,name ="about"), 
   path('help/',views.help,name="help"),
   path('login/',views.login.as_view(), name="login"),
   path('login1/',views.login1, name="login1")

]
