# analysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.upload_conversation, name='upload_conversation'),
    path('analyse/<int:conv_id>/', views.analyse_conversation, name='analyse_conversation'),
    path('reports/', views.AnalysisListView.as_view(), name='analysis_list'),
]
