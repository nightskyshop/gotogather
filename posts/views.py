from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)
from django.urls import reverse
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from posts.forms import ClassForm
from .models import Post, Class, Lesson, Comment
from .forms import PostForm, ClassForm, LessonForm, CommentForm

# Create your views here.
class IndexView(ListView):
  model = Class
  template_name = "class/index.html"
  context_object_name = "classes"
  paginate_by = 6
  ordering = ["-dt_created"]


class ClassCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Class
  template_name = "class/class_form.html"
  form_class = ClassForm

  redirect_unauthenticated_users = True
  raise_exception = True
  
  def get_success_url(self):
    return reverse('index')
  
  def test_func(self, user):
    return user.is_superuser
    

class LessonListView(ListView):
  model = Lesson, Class
  template_name = "class/lesson_list.html"
  context_object_name = "lessons"
  pk_url_kwarg = "class_id"
  paginate_by = 9

  def get_queryset(self):
    class_id = self.kwargs.get("class_id")
    return Lesson.objects.filter(upclass__id=class_id).order_by("-dt_created")
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    class_id = self.kwargs.get("class_id")
    context["class"] = Class.objects.get(id=class_id)
    return context


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Lesson, Class
  template_name = "class/lesson_form.html"
  pk_url_kwarg = "class_id"
  lookup_url_kwarg = "lesson_id"
  form_class = LessonForm

  redirect_unauthenticated_users = True
  raise_exception = True

  def form_valid(self, form):
    class_id = self.kwargs.get("class_id")
    class_title = Class.objects.get(id=class_id)
    form.instance.upclass = class_title
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    class_id = self.kwargs.get("class_id")
    context["upclass"] = Class.objects.get(id=class_id).id
    return context
  
  def get_success_url(self):
    class_id = self.kwargs.get("class_id")
    return reverse('class-detail', kwargs={"class_id": class_id})
  
  def test_func(self, user):
    return user.is_superuser


class PostListView(ListView):
  model = Post, Lesson, Class
  template_name = "posts/post_list.html"
  ordering = ['-dt_created']
  context_object_name = "posts"
  paginate_by = 6
  lookup_url_kwarg = "class_id"
  pk_url_kwarg = "lesson_id"

  def get_queryset(self):
    lesson_id = self.kwargs.get("lesson_id")
    return Post.objects.filter(uplesson__id=lesson_id).order_by("-dt_created")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    context["lesson"] = Lesson.objects.get(id=lesson_id)
    context["class"] = Class.objects.get(id=class_id)
    return context


class PostDetailView(DetailView, CreateView):
  model = Post
  template_name = "posts/post_detail.html"
  context_object_name = "comments"
  ordering = ['-dt_created']
  lookup_url_kwarg = "lesson_id"
  lookup_field = "class_id"
  pk_url_kwarg = "post_id"
  form_class = CommentForm

  def form_valid(self, form):
    post_id = self.kwargs.get("post_id")
    post_title = Post.objects.get(id=post_id)
    form.instance.uppost = post_title
    form.instance.author = self.request.user
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post_id = self.kwargs.get("post_id")
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    context["post"] = Post.objects.get(id=post_id)
    context["lesson"] = Lesson.objects.get(id=lesson_id)
    context["class"] = Class.objects.get(id=class_id)
    context["comments"] = Comment.objects.filter(uppost__id=post_id)
    return context
  
  def get_success_url(self):
    class_id = self.kwargs.get("class_id")
    lesson_id = self.kwargs.get("lesson_id")
    post_id = self.kwargs.get("post_id")
    return reverse('post-detail', kwargs={"class_id": class_id, "lesson_id": lesson_id, "post_id": post_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Comment
  lookup_url_kwarg = "lesson_id"
  lookup_field = "class_id"
  pk_url_kwarg = "comment_id"

  redirect_unauthenticated_users = True
  raise_exception = True

  def get(self, *args, **kwargs):
    return self.post(*args, **kwargs)

  def get_success_url(self):
    post_id = self.kwargs.get("post_id")
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    return reverse('post-detail', kwargs={"class_id": class_id, "lesson_id": lesson_id, "post_id": post_id})
  
  def test_func(self, user):
    post = self.get_object()
    if (user.is_superuser):
      return True
    return post.author == user


class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  template_name = "posts/post_form.html"
  lookup_url_kwarg = "lesson_id"
  lookup_field = "pk"
  pk_url_kwarg = "class_id"
  form_class = PostForm

  redirect_unauthenticated_users = True
  raise_exception = True

  def form_valid(self, form):
    lesson_id = self.kwargs.get("lesson_id")
    lesson_title = Lesson.objects.get(id=lesson_id)
    form.instance.uplesson = lesson_title
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    context["lesson"] = Lesson.objects.get(id=lesson_id)
    context["class"] = Class.objects.get(id=class_id)
    return context

  def get_success_url(self):
    class_id = self.kwargs.get("class_id")
    lesson_id = self.kwargs.get("lesson_id")
    return reverse('post-list', kwargs={"class_id": class_id, "lesson_id": lesson_id})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  template_name = "posts/post_form.html"
  lookup_url_kwarg = "lesson_id"
  lookup_field = "class_id"
  pk_url_kwarg = "post_id"
  form_class = PostForm

  redirect_unauthenticated_users = True
  raise_exception = True

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post_id = self.kwargs.get("post_id")
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    context["post"] = Post.objects.get(id=post_id)
    context["lesson"] = Lesson.objects.get(id=lesson_id)
    context["class"] = Class.objects.get(id=class_id)
    return context

  def get_success_url(self):
    class_id = self.kwargs.get("class_id")
    lesson_id = self.kwargs.get("lesson_id")
    post_id = self.kwargs.get("post_id")
    return reverse('post-detail', kwargs={"class_id": class_id, "lesson_id": lesson_id, "post_id": post_id})
  
  def test_func(self, user):
    post = self.get_object()
    if (user.is_superuser):
      return True
    return post.author == user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = "posts/post_confirm_delete.html"
  lookup_url_kwarg = "lesson_id"
  lookup_field = "class_id"
  pk_url_kwarg = "post_id"

  redirect_unauthenticated_users = True
  raise_exception = True

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post_id = self.kwargs.get("post_id")
    lesson_id = self.kwargs.get("lesson_id")
    class_id = self.kwargs.get("class_id")
    context["post"] = Post.objects.get(id=post_id)
    context["lesson"] = Lesson.objects.get(id=lesson_id)
    context["class"] = Class.objects.get(id=class_id)
    return context

  def get_success_url(self):
    class_id = self.kwargs.get("class_id")
    lesson_id = self.kwargs.get("lesson_id")
    return reverse('post-list', kwargs={"class_id": class_id, "lesson_id": lesson_id})

  def test_func(self, user):
    post = self.get_object()
    if (user.is_superuser):
      return True
    return post.author == user


class CommentaryView(ListView):
  model = Post
  template_name = "class/commentary.html"


class CustomPasswordChangeView(PasswordChangeView):
  def get_success_url(self):
    return reverse('index')