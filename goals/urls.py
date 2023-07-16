from django.urls import path

from goals.views.goal_category_views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryDetailsView
from goals.views.goal_views import GoalCreateView, GoalListView, GoalDetailsView
from goals.views.goal_comment_view import GoalCommentDetailsView, GoalCommentListView, GoalCommentCreateView
from goals.views.boards import BoardListView, BoardCreateView, BoardDetailView

urlpatterns = [
    # board
    path('board/create', BoardCreateView.as_view(), name='create_board'),
    path('board/list', BoardListView.as_view(), name='list_boards'),
    path('board/<int:pk>', BoardDetailView.as_view(), name='board_details'),
    # categories
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='create_category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='list_categories'),
    path('goal_category/<int:pk>', GoalCategoryDetailsView.as_view(), name='category_details'),
    # goals
    path('goal/create', GoalCreateView.as_view(), name='create_goal'),
    path('goal/list', GoalListView.as_view(), name='list_goals'),
    path('goal/<int:pk>', GoalDetailsView.as_view(), name='goal_details'),
    # comments
    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create_comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='list_comment'),
    path('goal_comment/<int:pk>', GoalCommentDetailsView.as_view(), name='comment_details'),
]
