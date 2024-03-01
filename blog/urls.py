from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post-new/', views.PostCreateView.as_view(), name="post_create"),
    path('post_edit/<slug>/', views.PostEdit.as_view(), name="post_edit"),
    path('post_delete/<slug>/', views.PostDelete.as_view(), name="post_delete"),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]