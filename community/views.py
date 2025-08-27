from django.shortcuts import render,redirect, get_object_or_404
from .models import  *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
import random
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, PostMedia, Comment
from .forms import  *
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import time
# Create your views here.
def home(request):
    return render(request, 'index.html')


# This view renders the community page where users can learn about the Beneath The Blue community and its mission.
def community_page(request):
    Category_data = Category.objects.all()
    # Try to get category id from GET, else use first category's id
    id = request.GET.get('category') or (Category_data.first().id if Category_data.exists() else None)
    try:
        Category_selected = Category.objects.get(id=id)
        Community_data = Community.objects.filter(category=Category_selected)
    except (Category.DoesNotExist, TypeError, ValueError):
        Category_selected = None
        Community_data = Community.objects.none()

    data = {
        'Community_data': Community_data,
        'Category_data': Category_data,
        'Category_selected': Category_selected
    }
    return render(request, 'community.html', data)


 
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/sign_in/')
def quiz(request):
    # Get all questions and shuffle them
    all_questions = list(Question.objects.all())
    random.shuffle(all_questions)
    
    # Store shuffled questions in session
    request.session['shuffled_questions'] = [q.id for q in all_questions]
    request.session['current_question_index'] = 0
    request.session['score'] = 0
    
    return render(request, 'quiz.html', {
        'question': all_questions[0]
    })

def next_question(request):
    if request.method == 'POST':
        # Process answer if submitted
        # You'll need to add this logic
        
        # Get next question
        current_index = request.session.get('current_question_index', 0)
        question_ids = request.session.get('shuffled_questions', [])
        
        if current_index + 1 < len(question_ids):
            next_question = Question.objects.get(id=question_ids[current_index + 1])
            request.session['current_question_index'] = current_index + 1
            return render(request, 'quiz.html', {
                'question': next_question
            })
        else:
            # Quiz completed
            score = request.session.get('score', 0)
            x= random.randint(1, 5)
            return render(request, 'result.html', {
                'score':   x,
                'total': len(question_ids),
                'wrong':10-x,
            })
    
    return redirect('quiz')




def explore_map(request):
    return  render(request, 'explore.html')


def threats(request):
    threats = Threat.objects.all()
    return render(request, 'threats-solution.html', {'threats': threats})


 
# sing in function
# from django.contrib.auth.models import User

def sign_in(request):
    if request.method == "POST":
        user_id = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'sign_in.html', {'error': 'Invalid credentials. Please try again.'})
    return render(request, "sign_in.html")

def sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'sign_up.html', {'error': 'Passwords do not match. Please try again.'})
        
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            return render(request, 'sign_up.html', {'error': 'User already exists. Please sign in.'})
        
        # Create user
        try:
            # Extract name from email (before @ and remove numbers)
            name = ''.join([c for c in email.split('@')[0] if not c.isdigit()])
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            user.save()
            
            # Authenticate and login
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        except Exception as e:
            return render(request, 'sign_up.html', {'error': f'Error creating account: {str(e)}'})
    
    return render(request, "sign_up.html")

@login_required(login_url='/sign_in/')
def community_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.filter(post__in=posts).order_by('-created_at')
    return render(request, 'community_posts.html', {'posts': posts, 'Comment':comments})

@login_required(login_url='/sign_in/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            files = request.FILES.getlist('media')
            for file in files:
                PostMedia.objects.create(post=post, file=file)
                
            return redirect('community_posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required(login_url='/sign_in/')
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'my_posts.html', {'posts': posts})

@login_required(login_url='/sign_in/')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            
            files = request.FILES.getlist('new_media')
            for file in files:
                PostMedia.objects.create(post=post, file=file)
                
            return redirect('my_posts')
    else:
        form = PostEditForm(instance=post)
    
    return render(request, 'edit_post.html', {
        'form': form,
        'post': post
    })

@login_required(login_url='/sign_in/')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required(login_url='/sign_in/')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})

@login_required(login_url='/sign_in/')
def delete_media(request, media_id):
    media = get_object_or_404(PostMedia, id=media_id, post__author=request.user)
    if request.method == 'POST':
        media.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required(login_url='/sign_in/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('community_posts')
    return redirect('community_posts')

@login_required(login_url='/sign_in/')
def submit_pledge(request):
    form = PledgeForm(request.POST)
    if form.is_valid():
        pledge = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Pledge submitted successfully!'
        })
    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)

@login_required(login_url='/sign_in/')
def submit_idea(request):
    form = IdeaForm(request.POST)
    if form.is_valid():
        idea = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Idea submitted successfully!'
        })
    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)

@login_required(login_url='/sign_in/')
def submit_feedback(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        feedback = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Feedback submitted successfully!'
        })
    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400) 

def endangered_species(request):
    animals = EndangeredSpecies.objects.all()
    return render(request, 'Endangered_species.html', {'animals': animals})

def ocean(request):
    animals = EndangeredSpecies.objects.all()
    return render(request, 'Endangered_species.html', {"animals": animals})

User = get_user_model()

def send_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session['otp_created_time'] = str(time.time())
            
            try:
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent successfully!')
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, f'Failed to send OTP: {str(e)}')
                return redirect('password_reset')
                
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address')
    return render(request, 'password_reset.html')

def verify_otp(request):
    if 'reset_otp' not in request.session:
        return redirect('password_reset')
        
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        if int(user_otp) == request.session['reset_otp']:
            # Check if OTP is expired (5 minutes)
            if time.time() - float(request.session['otp_created_time']) > 300:
                messages.error(request, 'OTP has expired')
                return redirect('password_reset')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')

def reset_password(request):
    if 'reset_email' not in request.session:
        return redirect('password_reset')
        
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            try:
                user = User.objects.get(email=request.session['reset_email'])
                user.set_password(password)
                user.save()
                
                # Clean up session
                del request.session['reset_otp']
                del request.session['reset_email']
                del request.session['otp_created_time']
                
                messages.success(request, 'Password reset successfully! Please login with your new password')
                return redirect('sign_in')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('password_reset')
    return render(request, 'reset_password.html')