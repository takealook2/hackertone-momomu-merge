from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.

# 어드민 페이지 내에서 가입한 유저들의 정보 확인 관련 
class BoardMember(models.Model):
    username    = models.CharField(max_length=100, verbose_name='유저이름')
    nickname    = models.CharField(max_length=100, verbose_name='유저닉네임')
    email       = models.EmailField(max_length=100, verbose_name='유저이메일')
    password    = models.CharField(max_length=100, verbose_name='유저PW')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='마지막수정일')

    def __str__(self):
        return self.email

    class Meta:
        db_table            = 'boardmembers'
        verbose_name        = '게시판멤버'
        verbose_name_plural = '게시판멤버'

# 게시판 관련 모델
class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    description = RichTextUploadingField(blank=True,null=True)
    body = models.TextField()
    image = models.ImageField(upload_to = "blog/", blank=True, null=True)

    def __str__(self):
        return self.title #제목으로 보이게
    
    def summary(self):
        return self.body[:100]

#댓글 관련 모델
class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author_name=models.CharField(max_length=20) 
    comment_text=models.TextField() 
    created_at=models.DateTimeField(default=timezone.now) #장고에서 기본으로 제공됨 
    # 들어갈 내용들 : 댓글 작성자, 댓글 내용, 댓글 작성 시간

    def approve(self):
        self.save()

    def __str__(self): 
        return self.comment_text
