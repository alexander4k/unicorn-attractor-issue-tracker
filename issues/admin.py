from django.contrib import admin
from .models import Issue, Comment, Upvote

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display=('title','author','status','issue_type', 'created', 'updated','completed', 'total_upvotes', 'total_comments')
    fields = ("title", "description", 'status','issue_type', 'created', 'updated','completed', 'author')
    readonly_fields=('created','updated', 'completed')
    
@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_filter=('related_issue',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter=('related_issue',)
