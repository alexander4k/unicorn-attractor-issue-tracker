from django.shortcuts import reverse
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage

from ..models import Issue

def filter_and_sort_issues(filter_by, sort_type=None):
    """
    Return a list of issues after its been filtered and/or sorted
    '.+' for 'filter_by' will return all issues,
    'BG' will return all bugs,
    'FR' will return all feature requests
    """
    filter_by = filter_by
    if sort_type == None:
        issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$'
            ).order_by('-updated')

    else:
        if sort_type == 'popular':
            issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$'
            ).annotate(number_of_upvotes=Count('upvotes')).order_by('-number_of_upvotes')
        elif sort_type == 'comments':
            issues_list = Issue.objects.filter(issue_type__regex=r'^' + str(filter_by) + '$'
            ).annotate(number_of_comments=Count('comments')).order_by('-number_of_comments')
    return issues_list
    
def pagination(item_list, page):
    """
    Used for limiting the number of items on page at one time
    """
    current_page = page
    paginator = Paginator(item_list, 10)
    try:
        issues = paginator.page(current_page)
    except InvalidPage:
        issues = paginator.page(1)
    
    return issues