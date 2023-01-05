from django.urls import path
from .views import SignUpView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailsView, ForgotPassWordView, PasswordResetConfirm, PasswordResetDone
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', LoginView.as_view(template_name='app1/login.html'), name='login'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('details/<int:pk>/', PostDetailsView.as_view(), name='details'),
    path('password_reset/', ForgotPassWordView.as_view(), name='forgot-password'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
]
