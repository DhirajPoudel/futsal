from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('tables/', views.tablePage, name="table"),
    path('addFutsal/', views.addFutsal, name="addFutsal"),
    path('approveBooking/<str:pk>/', views.approveBooking, name="approve_booking"),
    path('rejectBooking/<str:pk>/', views.rejectBooking, name="reject_booking"),
]

