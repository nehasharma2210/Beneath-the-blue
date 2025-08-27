from django.db import models
from django.contrib.auth.models import User

# loging
class loging(models.Model):
    user_id = models.EmailField()
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user_id

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Community(models.Model):
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='communities')
    link = models.URLField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    

# from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Threat(models.Model):
    image = models.ImageField(upload_to='threats/', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    # solution = models.TextField()
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title

class   Solution(models.Model):
    image = models.ImageField(upload_to='solutions/', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    # solution = models.TextField()
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(loging, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(loging, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.user_id} on {self.post.title}'

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, through='Like')
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

class PostMedia(models.Model):
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    

from django.core.validators import MinValueValidator, MaxValueValidator

# index posts
class Pledge(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    eliminate_plastics = models.BooleanField(default=False)
    sustainable_seafood = models.BooleanField(default=False)
    join_cleanups = models.BooleanField(default=False)
    reduce_footprint = models.BooleanField(default=False)
    support_conservation = models.BooleanField(default=False)
    personal_promise = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pledge by {self.name}"

class Idea(models.Model):
    CATEGORY_CHOICES = [
        ('pollution', 'Pollution Solutions'),
        ('research', 'Marine Research'),
        ('education', 'Ocean Education'),
        ('tech', 'Conservation Tech'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Idea: {self.title} by {self.name}"

class Feedback(models.Model):
    FEEDBACK_TYPE = [
        ('explorer', 'Depth Explorer'),
        ('education', 'Learning Content'),
        ('action', 'Take Action'),
        ('general', 'General Feedback'),
    ]
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPE)
    message = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback ({self.get_feedback_type_display()}) - Rating: {self.rating}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
# spices
class endangered_species(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class EndangeredSpecies(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    audio = models.FileField(upload_to='audios/')
    des=models.TextField(default='No description available')
    threat = models.ForeignKey(endangered_species, on_delete=models.CASCADE, related_name='endangered_species')
    url=models.URLField(blank=True, null=True)