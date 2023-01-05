from django.shortcuts import render, redirect, get_object_or_404
from .forms import MyUserCreationForm, LoginForm, PostForm
from django import views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Post
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .permissions import IsOwnerMixin
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


class SignUpView(CreateView):
    model = User
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app1/signup.html'


# class SignUpView(views.View):
#     template_name = 'app1/signup.html'
#     form_class = MyUserCreationForm
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template_name, context={'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         return render(request, self.template_name, context={'form': form})


class LoginView(views.View):
    form_class = LoginForm
    template_name = 'app1/login.html'

    def get(self, request):
        if request.user and request.user.is_authenticated:
            return redirect('posts')
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        next_url = request.GET.get('next')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('posts')
        return render(request, self.template_name, context={'form': form})


class LogoutView(views.View):

    def get(self, request):
        logout(request)
        return redirect('login')


class PostListView(LoginRequiredMixin, ListView):
    model = Post


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name = 'app1/post_update.html'


class PostDeleteView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')


class PostDetailsView(LoginRequiredMixin, DetailView):
    model = Post


class ForgotPassWordView(views.View):
    form_class = PasswordResetForm
    template_name = "app1/forgot_password.html"

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(subject_template_name='app1/password_reset_subject.txt',
                      email_template_name='app1/password_reset_email.html', request=request)
            return redirect('login')
        context = {'form': form}
        return render(request, self.template_name, context)


class PasswordResetConfirm(views.View):
    form_class = SetPasswordForm
    template_name = 'app1/password_reset_form.html'

    def get(self, request, uidb64, token):
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User,pk=user_id)
        if default_token_generator.check_token(user, token):
            form = self.form_class(user=user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, uidb64, token):
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=user_id)
        form = self.form_class(user, request.POST)
        if form.is_valid():
            print("hellooo")
            form.save()
            return redirect('password_reset_done')
        context = {'form': form}
        return render(request, self.template_name, context)


class PasswordResetDone(views.View):
    template_name = 'app1/password_reset_done.html'

    def get(self, request):
        return render(request, self.template_name)






