from django.urls import path
from . import views

urlpatterns = [
    path('issues', views.IssueListView.as_view(), name='myissues'),
    path('queries', views.QueryListView.as_view(), name='myqueries'),
    path('feedbacks', views.FeedbackListView.as_view(), name='myfeedbacks'),
    path('issue/submit', views.IssueCreateView.as_view(), name='submit_issue'),
    path('query/submit', views.QueryCreateView.as_view(), name='submit_query'),
    path('feedback/submit', views.FeedbackCreateView.as_view(), name='submit_feedback'),
    path('issue/<int:pk>/', views.IssueDetailView.as_view(), name='issue_details'),
    path('query/<int:pk>/', views.QueryDetailView.as_view(), name='query_details'),
    path('feedback/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_details'),
    path('issue/<int:pk>/update', views.IssueUpdateView.as_view(), name='update_issue'),
    path('query/<int:pk>/update', views.QueryUpdateView.as_view(), name='update_query'),
    path('feedback/<int:pk>/update', views.FeedbackUpdateView.as_view(), name='update_feedback'),
    path('issue/<int:pk>/comment/add', views.IssueCommentCreateView.as_view(), name='add_issue_comment'),
    path('query/<int:pk>/comment/add', views.QueryCommentCreateView.as_view(), name='add_query_comment'),
    path('feedback/<int:pk>/comment/add', views.FeedbackCommentCreateView.as_view(), name='add_feedback_comment'),
]
