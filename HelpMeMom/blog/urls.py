from django.urls import path,include
from . import views
from .views import UserPostListView, PostListView, PostDeleteView, PostDetails, PostCreateView, PostUpdateView, CommentDeleteView, CommentUpdateView, SearchPost

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',PostListView.as_view(),name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    # path('post/<int:pk>',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:post_pk>', PostDetails, name='post-detail'),
    path('about/',views.about, name='blog-about'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(template_name='blog/post_confirm_delete.html'),name='post-delete'),
    path('comment/<int:pk>/update',CommentUpdateView.as_view(),name='comment-update'),
    path('comment/<int:pk>/delete',CommentDeleteView.as_view(template_name='blog/comment_delete.html'),name='comment-delete'),
    path('search/',SearchPost,name='search-stuff'),
    path('api/',views.ApiSearch,name='api'),
    # path('analytics/',Analytics,name='admin-anals'),
    # path('vidcall/',views.some_view,name='vid'),
]
