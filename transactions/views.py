from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required
def begin_purchase(request):
    """
    View for the start of purchase
    Get the number of upvotes a user wants to buy and
    saves it in session for use with the continue_purchase view
    """
    if request.method == 'POST':
        upvotes_amount = int(request.POST.get('upvotes_amount'))
        request.session['purchase'] = upvotes_amount
        return redirect("continue_purchase")
    
    return render(request, "begin_purchase.html")
    
@login_required    
def continue_purchase(request):
    """
    View for completing the purchase using Stripe
    Takes the number of upvotes from session and uses it to calculate how
    much to charge the customer
    
    """
    upvotes_amount = int(request.session['purchase'])
    
    if request.method=="POST":
        if "stripeToken" in request.POST:
            try:
                # Try to charge the customer using given card details entered
                # for the amount of upvotes given
                customer = stripe.Charge.create(
                    amount = upvotes_amount * 500,
                    currency = "EUR",
                    description = '{} upvotes for {}'.format(
                                                        upvotes_amount,
                                                        request.user.email
                                                        ),
                    source = "tok_visa",
                    statement_descriptor='{} upvotes'.format(upvotes_amount),
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            if customer.paid:
                # If transaction was successfull, increase the user profile's
                # upvotes amount
                profile = request.user.profile
                profile.upvotes_owned += upvotes_amount
                profile.save()
                return redirect('finish_purchase')
            else:
                messages.error(request, "Unable to take payment")
        else:
            return render(request, "continue_purchase.html", 
                {
                    'publishable': settings.STRIPE_PUBLISHABLE,
                    'upvotes_amount': upvotes_amount,
                })
            
    return render(request, "continue_purchase.html", 
        {
            "total_price": upvotes_amount * 5,
            "upvotes_amount": upvotes_amount
        })
    
@login_required        
def finish_purchase(request):
    """
    View to display page once purchase is finished
    """
    upvotes_owned = request.user.profile.upvotes_owned
    return render(request, "finish_purchase.html", 
        {
            "upvotes_owned": upvotes_owned
        })