from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
from blogs.models import Post, Blog, Tag, Category
from django.urls import reverse
from .forms import BlogSearchForm, PostCreateForm, PostEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

class IsAuthorOrStuffMixin():
    is_create_post = False

    def get(self, *args, **kwargs):
        self.object = None

        if self.is_create_post:
            try:
                self.object = self.get_object(queryset=Blog.objects.all())
                # jesli obj nie istnieje - 404 error a nie raise
            except Post.DoesNotExist as e:
                return redirect('blogs:view-blog', self.kwargs.get('slug'))
        else:
            self.object = self.get_object()
        
        if not self.object.is_owner(self.request.user) and not (self.request.user.is_staff or self.request.user.is_superuser):
            view = 'blogs:view-blog' if isinstance(self.object, Blog) else 'blogs:post-detail'
            return redirect(view, slug=self.object.slug)
        return super().get(*args, **kwargs)

class IsOwnerMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.object.is_owner(self.request.user)
        return context

class PostView(IsOwnerMixin, DetailView):
    model = Post
    template_name = 'blogs/blog_post.html'

class PostCreate(LoginRequiredMixin, IsAuthorOrStuffMixin, CreateView):
    model = Post
    template_name = 'blogs/post_create.html'
    # fields = ['title', 'content', 'tags']
    form_class = PostCreateForm
    is_create_post = True

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:post-detail', args=[self.object.slug])
    
    def form_valid(self, form):
        creator = get_object_or_404(User, pk=self.request.user.pk)
        blog = get_object_or_404(Blog, slug=self.kwargs.get('slug'))

        form.instance.creator = creator
        form.instance.blog = blog
        return super().form_valid(form)

class PostUpdate(IsAuthorOrStuffMixin, UpdateView):
    model = Post
    template_name = 'blogs/post_edit.html'
    form_class = PostEditForm
    # fields = ['title', 'content', 'tags']

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:post-detail', args=[self.object.slug])

class PostDelete(IsAuthorOrStuffMixin, DeleteView):
    model = Post
    template_name = 'blogs/post_delete.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:view-blog', args=[self.object.blog.slug])

class BlogList(ListView):
    # model = Blog
    context_object_name = "blogs"
    template_name = "blogs/blog_list_exp.html"
    form_class = BlogSearchForm
    form_instance = None
    paginate_by = 5

    def get_queryset(self):
        self.form_instance = self.form_class(self.request.GET)
        
        if self.form_instance.is_valid():
            a = self.form_instance.cleaned_data
            cat = a['category'] # Category model class / None
            title = a['search'] # str / ''
            if cat is not None and len(title) > 0:
                return Blog.objects.filter(category__exact=cat, name__contains=title)
            elif cat is None:
                return Blog.objects.filter(name__contains=title)
            elif len(title) is 0:
                return Blog.objects.filter(category__exact=cat)
            
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_instance
        context['url_prefix'] = ''

        if "search" in self.request.GET:
            context['url_prefix'] += f"search={self.request.GET['search']}&"
        if "category" in self.request.GET:
            context['url_prefix'] += f"category={self.request.GET['category']}&"

        return context

class BlogView(IsOwnerMixin, DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = "blogs/blog_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_posts"] = Post.objects.filter(blog__pk=self.object.id)
        return context

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['category', 'name', 'description']
    template_name = 'blogs/blog_create.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:view-blog', args=[self.object.slug])

    def form_valid(self, form):
        creator = get_object_or_404(User, pk=self.request.user.pk)

        form.instance.creator = creator
        return super().form_valid(form)

class BlogEdit(IsAuthorOrStuffMixin, UpdateView):
    model = Blog
    template_name = "blogs/blog_edit.html"
    fields = ['category', 'name', 'description']

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:view-blog', args=[self.object.slug])

class BlogDelete(IsAuthorOrStuffMixin, DeleteView):
    model = Blog
    template_name = "blogs/blog_delete.html"

    def get_success_url(self, *args, **kwargs):
        return reverse('blogs:blogs-explore')

class ProfileView(DetailView):
    model = User
    template_name = 'blogs/profile.html'
    context_object_name = 'account'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.filter(creator=self.object)
        return context

class RegisterView(CreateView):
    model = User
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = '/v/b/explore'
    
    def form_valid(self, form):
        q = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            print(username, password)
        else:
            print('NO LOGIN')
        return q