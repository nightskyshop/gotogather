from django.urls import path
from . import views

urlpatterns = [
  # class
	path('', views.IndexView.as_view(), name='index'),
  path('class/new/', views.ClassCreateView.as_view(), name='class-create'),
  path('classes/<int:class_id>/', views.LessonListView.as_view(), name='class-detail'),
  path('classes/<int:class_id>/lesson/new', views.LessonCreateView.as_view(), name='lesson-create'),
  
  # post
  path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/', views.PostListView.as_view(), name='post-list'),
	path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/new/', views.PostCreateView.as_view(), name='post-create'),
	path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
	path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='post-update'),
	path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

  # comment
  path('classes/<int:class_id>/lesson/<int:lesson_id>/posts/<int:post_id>/comment/<int:comment_id>/delete', views.CommentDeleteView.as_view(), name='comment-delete'),

  # commentary
  path('commentary', views.CommentaryView.as_view(), name='commentary')
]