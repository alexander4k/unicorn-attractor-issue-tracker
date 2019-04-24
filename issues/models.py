from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class Issue(models.Model):
    TYPE_CHOICES = (
        ("BG", "Bug"),
        ("FR", "Feature"),
    )
    STATUS_CHOICES = (
        ("IC", "Incomplete"),
        ("IP", "In-progress"),
        ("CT", "Complete"),
    )
    title = models.CharField(max_length=254, default="")
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="IC")
    issue_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="BG")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
        
    def __str__(self):
        return self.title
          
    @property
    def total_upvotes(self):
        return self.upvotes.count
        
    @property
    def total_comments(self):
        return self.comments.count
        
    @property 
    def status_long(self):
        return self.get_status_display()
      
class Upvote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    related_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='upvotes')
    
    def __str__(self):
        return 'Upvote on %s by %s' % (self.related_issue.title, self.author.username)
        
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    related_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    def __str__(self):
        return 'Comment on %s by %s' % (self.related_issue.title, self.author.username)
        
@receiver(pre_save, sender=Issue)
def set_date_on_status_change(sender, instance, **kwargs):
    """ 
    Called while an issue is being saved, compares the new version of an issue
    to the version before it was saved for changes on status
    When changing the status of an issue, update the 'completed' and 'updated' fields
    if the status is changed to 'Complete' otherwise update just the 'updated' field
    """
    try:
        original_issue = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if original_issue.status != instance.status and instance.status == "CT":
            instance.completed = timezone.now()
            instance.updated = timezone.now()
        elif original_issue.status != instance.status:
            instance.updated = timezone.now()
