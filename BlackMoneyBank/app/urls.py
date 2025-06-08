from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name="register"),
    path('home/', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('accdetails/', views.accdetails, name='accdetails'),
    path('pin/', views.pin_generation, name='pin'),
    path('balance/', views.balance, name='balance'),
    path('deposite/', views.deposite, name='deposite'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('acctransfer/', views.acc_transfer, name='acctransfer'),
    path('delete-all/', views.delete_all_records, name='delete_all_records'),
]