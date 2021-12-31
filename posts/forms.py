from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Class, Lesson, Comment


class ClassForm(forms.ModelForm):

  class Meta:
    model = Class
    fields = ['title']
    widgets = {
      'title': forms.TextInput(attrs={
        'class': 'title',
        'placeholder': '제목을 입력하세요'})
    }

class LessonForm(forms.ModelForm):

  class Meta:
    model = Lesson
    fields = ['title']
    widgets = {
      'title': forms.TextInput(attrs={
        'class': 'title',
        'placeholder': '제목을 입력하세요'})
    }

class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = [
      'title',
      'content',
      'image1',
      'image2',
      'image3',
    ]
    widgets = {
      'title': forms.TextInput(attrs={
        'class': 'title',
        'placeholder': '책이름 숫자 (예: 레미제라블5)'}),

      'content': forms.Textarea(attrs={
        'placeholder': '내용을 입력하세요'})
      }

  def clean_title(self):
    title = self.cleaned_data['title']
    if '*' in title:
      raise ValidationError('* 는 포함될 수 없습니다.')
    return title

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']
    widgets = {
      'comment': forms.TextInput(attrs={
        'placeholder': '댓글을 입력하세요'}),
      }