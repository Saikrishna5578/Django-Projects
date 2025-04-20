from django.urls import path
from . import views

urlpatterns =[
    path('',views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('home/', views.home, name='home'),
    path('list/', views.list, name='list'),
    path('history/', views.history, name='history'),
    path('edit/<int:p>',views.edit, name='edit'),
    path('delete/<int:id>',views.delete, name='delete'),
    path('task/<int:id>',views.task, name='task'),
    path('notask/<int:id>',views.notask, name='notask'),
]