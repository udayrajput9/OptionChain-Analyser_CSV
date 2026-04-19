from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('stock/<str:stock>/reset/', views.StockResetView.as_view(), name='reset_stock'),
    path('stock/<str:stock>/delete/', views.StockDeleteView.as_view(), name='delete_stock'),
    path('report/<str:stock>/<int:date>/', views.ReportView.as_view(), name='report'),
    path('prediction/<str:stock>/<int:date>/', views.PredictionView.as_view(), name='prediction'),
    path('outcome/<str:stock>/<str:date>/', views.OutcomeFeedView.as_view(), name='outcome_feed'),
    path('learning-report/<str:stock>/<str:date>/', views.LearningReportView.as_view(), name='learning_report'),
    # path('brain-memory/<str:stock>/', views.BrainMemoryView.as_view(), name='brain_memory'),
    # path('leaderboard/<str:stock>/', views.AlgoLeaderboardView.as_view(), name='algo_leaderboard'),
    # path('api/run-super-brain/', views.RunSuperBrainAPI.as_view(), name='api_super_brain'),
]
