from issues.models import Issue
from django.utils import timezone
from dateutil.relativedelta import relativedelta

def get_previous_dates(months, days, range_end):
    """
    Used to get a list of dates starting from specified point and going backwards
    
    Takes in expressions in string form to allow the passing of variable 'i' of the for loop
    in function arguments
    Given '-i' for the 'months' argument, '0' for 'days' and 12 for 'range_end',
    will add a date for each month starting from the previous one for 12 months
    
    Used with the get_issues_per_timerange function to filter through issues
    """
    previous_dates = []
    
    for i in range(1, range_end):
        date = timezone.now() + relativedelta(months=eval(months), days=eval(days))
        previous_dates.append(date)
    return previous_dates

def get_issues_per_timerange(previous_dates):
    """
    Filters issues by dates and adds them to a list. 
    Used to get issue count for each day for last 7 days and
    if there are more than 7 dates, each month over last 12 months for
    display on a bar chart.
    """
    previous_dates = previous_dates
    issues_per_timerange = []
    for date in previous_dates:
        if len(previous_dates) > 7:
            issues_count = Issue.objects.filter(completed__month=date.month, completed__year=date.year).count()
        else:
            issues_count = Issue.objects.filter(completed__month=date.month, completed__year=date.year, completed__day=date.day).count()
        issues_per_timerange.append(issues_count)
    return issues_per_timerange
    
def get_count_of_issues_by_status():
    """
    Get the count of issues for each status and save to a list
    Used for the pie chart
    """
    status_list = ["CT", "IP", "IC"]
    
    count_list = []
    for status in status_list:
        issues_count = Issue.objects.filter(status=status).count()
        count_list.append(issues_count)
    return count_list