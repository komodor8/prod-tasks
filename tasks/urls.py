from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.IndexTaskView.as_view(), name='index'),
    path('create/', views.CreateTaskView.as_view(), name='create'),
    path('<int:pk>/', views.DetailTaskView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete'),
    path('<int:pk>/share/', views.ShareTaskView.as_view(), name='share'),
    path(
        '<int:task>/comments/create/',
        views.CreateCommentView.as_view(),
        name='comments-create'
    ),
    path(
        '<int:task>/comments/<int:pk>/delete/',
        views.DeleteCommentView.as_view(),
        name='comments-delete'
    ),
    path(
        '<int:task>/comments/<int:pk>/update/',
        views.UpdateCommentView.as_view(),
        name='comments-update'
    ),
]
