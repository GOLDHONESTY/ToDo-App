from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_todo, name='logout'),
    path('deletetask/<int:id>', views.DeleteTask, name='delete'),
    path('deletealltask', views.DeleteAllTask, name='deleteall'),
    path('update/<int:id>', views.Update, name='update'), 
]