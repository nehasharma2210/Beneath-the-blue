"""Beneath_the_blue URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from community.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # base urls
    path('admin/', admin.site.urls),
    path('',home, name="home"),
    path('sign_in/',sign_in, name="sign_in"),
    path('sign_up/',sign_up, name="sign_up"),
    path('logout/', user_logout, name='user_logout'),
    path('password-reset/', send_otp, name='password_reset'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),

    # community url
    path('community/',community_page, name="community_page"),
    path('explore_map/',explore_map, name="explore_map"),

    # quiz 
    path('quiz/', quiz, name='quiz'),
    path('next/', next_question, name='next_question'),

    path('threats/', threats, name='threats'),
    path('endangered_species/', endangered_species, name='endangered_species'),

    # home page related 
    path('submit-pledge/', submit_pledge, name='submit_pledge'),
    path('submit-idea/', submit_idea, name='submit_idea'),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),

    # post  related 
    path('CommunityPost/', community_posts, name='community_posts'),
    path('create-post/', create_post, name='create_post'),
    path('my-posts/', my_posts, name='my_posts'),
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('media/<int:media_id>/delete/', delete_media, name='delete_media'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    ]
# Serve media files in both development and production
from django.views.static import serve
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # In production, serve media files through Django
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
