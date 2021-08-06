from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models import *
from .models import Blog
from django.utils import timezone
from .forms import BlogForm
from .forms import CommentForm
from django.core.paginator import Paginator

# def home(request):
#     user_id = request.session.get('user')
#     #print(user_id)
#     if user_id:
#         member = BoardMember.objects.get(pk=user_id)
#         return HttpResponse(member.username)

#     return render(request, 'board.html')

# 로그인 관련 함수
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        res_data ={}

        if not (email and password):
            res_data['error'] = '모든 값을 입력하세요!'

        else:
            member = BoardMember.objects.get(email=email)
            #print(member.id)

            if check_password(password, member.password):
                request.session['user'] = member.id
                return render(request, 'board.html')

            else:
                res_data['error'] = '비밀번호가 일치하지 않습니다.'

        return render(request, 'home.html', res_data)

#로그아웃 함수
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')

#회원가입 관련 함수
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        #print (request.POST)
        username    = request.POST.get('username', None)
        #print(username)
        password    = request.POST.get('password', None)
        #print(password)
        re_password = request.POST.get('re_password', None)
        #print(re_password)
        email       = request.POST.get('email', None)
        nickname    = request.POST.get('nickname', None)
        res_data = {}

        # 별명, 이메일 중복 확인(비밀번호 맞는지 아닌지 여부 확인)

        if BoardMember.objects.filter(nickname=request.POST['nickname']).exists():
            res_data['error'] = '이미 존재하는 별명입니다.'
            print(res_data)
            return render(request, 'register.html', res_data)

        if BoardMember.objects.filter(email=request.POST['email']).exists():
            res_data['error'] = '이미 존재하는 이메일입니다.'
            print(res_data)
            return render(request, 'register.html', res_data)


        if password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
            print(res_data)
        
            return render(request, 'register.html', res_data)

        else:
            member = BoardMember(
                username    = username,
                nickname    = nickname,
                email       = email,
                password    = make_password(password)
            )
            member.save()
            return render(request, 'register_done.html', res_data)

# 홈(게시판 홈)
def board(request):
    blogs = Blog.objects.all().order_by('-id') # 블로그의 객체들을 가져와야함
    paginator = Paginator(blogs, 3) # 한 페이지에 몇 개 들어갈 건지
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'board.html', {'blogs':blogs})

# 게시글 detail 
def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    return render(request, 'detail.html', {'blog':blog})

# 새글작성인 new.html 보여줌
def new(request):
    form = BlogForm()
    return render(request, 'new.html', {'form':form})

# 새글을 데이터베이스에 저장
def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False) #임시저장(pubdate)
        new_blog.pub_date = timezone.now()
        new_blog.save()
        return redirect('detail', new_blog.id)
    return redirect('board')
    # new_blog = Blog()
    # new_blog.title = request.POST['title']
    # new_blog.writer = request.POST['writer']
    # new_blog.body = request.POST['body']
    # new_blog.pub_date = timezone.now()
    # new_blog.image = request.FILES['image']
    # new_blog.save()
    # return redirect('detail', new_blog.id)

# 수정기능 edit.html 보여줌
def edit(request, id):
    edit_blog = Blog.objects.get(id=id)
    return render(request, 'edit.html', {'blog':edit_blog})

# 수정 내용을 데이터베이스에 저장
def update(request, id):
    update_blog = Blog.objects.get(id = id)
    update_blog.title = request.POST['title']
    update_blog.writer = request.POST['writer']
    update_blog.body = request.POST['body']
    update_blog.pub_date = timezone.now()
    update_blog.save() # 필수!
    return redirect('detail', update_blog.id)

# 삭제하기 기능
def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('board')

# def comment(request, id):
#     blog = get_object_or_404(Blog, pk = id)
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = blog
#         comment.save()
#         return redirect('detail', id)
#     else:
#         form = CommentForm()
#     return redirect(request, 'comment.html', {'form':form})

#댓글 기능
def comment(request, id): 
    blog = get_object_or_404(Blog, pk = id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = blog
        comment.save()
        return redirect('detail', blog.id)
    else:
        form = CommentForm()
    return render(request, "comment.html", {'form':form})
