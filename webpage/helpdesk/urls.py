from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('log-in/', views.log_in, name='log-in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('check-ticket-status/', views.check_ticket_status, name='check-ticket-status'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('user-tickets/', views.user_tickets, name='user-tickets'),
    path('agent-log-in/', views.agent_log_in, name='agent-log-in'),
    path('agent-ticket-details/', views.agent_tickets, name='agent-ticket-details'),
    path('ticket-details/', views.ticket_details, name='ticket-details'),
    path('help-support/', views.help_support, name='help-support'),
               ]