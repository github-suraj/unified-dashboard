from django.urls import path
from . import views

urlpatterns = [
    path('issue/submit', views.IssueCreateView.as_view(), name='submit_issue'),
    path('query/submit', views.QueryCreateView.as_view(), name='submit_query'),
    path('feedback/submit', views.FeedbackCreateView.as_view(), name='submit_feedback'),
]
