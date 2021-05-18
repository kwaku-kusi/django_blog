from django.urls import path
from .views import PostListView, post_detail, post_share
app_name = "blog"

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('<year>/<month>/<day>/<post_slug>/', post_detail, name="post_detail"),
    path('<post_id>/share/', post_share, name="post_share")
]