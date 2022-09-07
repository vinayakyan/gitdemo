from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, LoginForm, PostForm
from django import views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Post
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .permissions import IsOwnerMixin


class SignUpView(views.View):
    template_name = 'app1/signup.html'
    form_class = MyUserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, context={'form': form})


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


class PostCreateView(LoginRequiredMixin, CreateView):
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





