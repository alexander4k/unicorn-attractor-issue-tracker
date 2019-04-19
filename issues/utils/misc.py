from django.shortcuts import reverse
from ..models import Issue
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage

def filter_and_sort_issues(filter_by, sort_type=None):
    filter_by = filter_by
    if not sort_type:
        issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$').order_by('-updated')
    else:
        if sort_type == 'popular':
            issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$').annotate(number_of_upvotes=Count('upvotes')).order_by('-number_of_upvotes')
        elif sort_type == 'comments':
            issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$').annotate(number_of_comments=Count('comments')).order_by('-number_of_comments')
    return issues_list
    
def pagination(issues_list, page):
    current_page = page
    paginator = Paginator(issues_list, 6)
    try:
        issues = paginator.page(current_page)
    except InvalidPage:
        issues = paginator.page(1)
    return issues