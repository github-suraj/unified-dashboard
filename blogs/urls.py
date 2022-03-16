from django.urls import path
from . import views

urlpatterns = [
    path('add_category/', views.add_category, name='add_category'),
    path('create/', views.BlogCreateView.as_view(), name='create_blog'),
    path('<int:pk>/', views.BLogDetailView.as_view(), name='blog_details'),
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='update_blog'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),
    path('<str:username>/', views.UserBlogListView.as_view(), name='user_blogs'),
]
