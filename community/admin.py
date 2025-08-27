from django.contrib import admin

# Register your models here.
from .models import *

# loging  display
class log(admin.ModelAdmin):
    list_display=('user_id','password')
admin.site.register(loging,log)
# Register the Community model with the admin site

# comminity section
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(Category,CategoryAdmin)

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('title','category','description')
admin.site.register(Community, CommunityAdmin)

# Register the Question, Option, and QuizResult models with the admin site
# 

admin.site.register(Question)
admin.site.register(Answer)

#  the Threat model  section
class ThreatAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
admin.site.register(Threat, ThreatAdmin)

#  endangered species section
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
admin.site.register(Solution, SolutionAdmin)



class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'total_likes_display')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content', 'location')
    inlines = [PostMediaInline]

    def total_likes_display(self, obj):
        return obj.likes.count()
    total_likes_display.short_description = 'Likes'

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('post', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('post__title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content', 'post__title')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'user__username')

admin.site.register(Pledge)
admin.site.register(Idea)
admin.site.register(Feedback)

# species
class  endangered_speciesAdmin(admin.ModelAdmin):
    list_display = ('title',)   
admin.site.register(endangered_species, endangered_speciesAdmin)

class EndangeredSpeciesAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo', 'audio', 'des', 'threat', 'url')  
admin.site.register(EndangeredSpecies, EndangeredSpeciesAdmin)