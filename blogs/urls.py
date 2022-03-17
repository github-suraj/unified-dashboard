from django.urls import path
from . import views

urlpatterns = [
    path('add_category/', views.add_category, name='add_category'),
    path('create/', views.BlogCreateView.as_view(), name='create_blog'),
    path('<int:pk>/', views.BLogDetailView.as_view(), name='blog_details'),
    path('<str:username>/', views.UserBlogListView.as_view(), name='user_blogs'),
    # path('<str:category>/', views.CategoryBlogListView.as_view(), name='category_blogs'),
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='update_blog'),
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),
    path('blog/<int:pk>/<str:opinion>/vote', views.BlogVoteView.as_view(), name='vote_blog'),
    path('comment/<int:pk>/add', views.BlogCommentView.as_view(), name='add_comment'),
    # path('comment/<int:pk>/update', views.BlogCommentUpdateView.as_view(), name='update_comment'),
    # path('comment/<int:pk>/delete', views.BlogCommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/<str:opinion>/vote', views.BlogCommentVoteView.as_view(), name='vote_blog_comment'),
]
