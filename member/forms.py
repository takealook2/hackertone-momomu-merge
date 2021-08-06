from django import forms #장고 제공
from .models import Blog #model에 맞는 데이터 형식을 만드는 거니깐
from .models import Comment
# 게시글 작성폼
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = ['title', 'writer', 'body', 'image'] #필드랑 연결
        # fields = ['title', 'writer', 'image', 'body', 'description']
        fields = ['title', 'writer', 'image', 'body']

# 댓글작성폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'comment_text']
