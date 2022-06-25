from django.urls import path, re_path

from goals import views


urlpatterns = [
    re_path(r'^goal_category/create/?$', views.GoalCategoryCreateView.as_view()),
    re_path(r'^goal_category/list/?$', views.GoalCategoryListView.as_view()),
    re_path(r'^goal_category/(?P<pk>[0-9]+)/?$', views.GoalCategoryView.as_view()),
    re_path(r'^goal/create/?$', views.GoalCreateView.as_view()),
    re_path(r'^goal/list/?$', views.GoalListView.as_view()),
    re_path(r'^goal/(?P<pk>[0-9]+)/?$', views.GoalRUDAView.as_view()),
    re_path(r'^goal_comment/create/?$', views.GoalCommentCreateView.as_view()),
    re_path(r'^goal_comment/list/?$', views.GoalCommentListView.as_view()),
    re_path(r'^goal_comment/(?P<pk>[0-9]+)/?$', views.GoalCommenRUDAView.as_view()),
    re_path(r'^board/create/?$', views.BoardCreateView.as_view()),
    re_path(r'^board/list/?$', views.BoardListView.as_view()),
    re_path(r'^board/(?P<pk>[0-9]+)/?$', views.BoardView.as_view()),
]