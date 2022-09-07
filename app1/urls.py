from django.urls import path
from .views import SignUpView, LoginView, PostListView, LogoutView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailsView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('details/<int:pk>/', PostDetailsView.as_view(), name='details'),
]
