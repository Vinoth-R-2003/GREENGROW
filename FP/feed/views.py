from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post
from .forms import PostForm

def index(request):
    form = PostForm()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')

    posts = Post.objects.all()
    return render(request, 'feed/index.html', {'posts': posts, 'form': form})

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })
@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    
    if content:
        comment = post.comments.create(author=request.user, content=content)
        return JsonResponse({
            'status': 'success',
            'author': comment.author.username,
            'content': comment.content,
        })
    return JsonResponse({'status': 'error', 'message': 'Content required'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Content required'}, status=400)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('index')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('index')
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            if request.POST.get('remove_image') == 'true':
                if edited_post.image:
                    edited_post.image.delete(save=False)
                    edited_post.image = None
            edited_post.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'feed/edit_post.html', {'form': form, 'post': post})
