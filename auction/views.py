from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Auction, Item, Comment, Cart, CartItem, Payment, Bid
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import PaymentForm
import stripe


def auction_dashboard(request):
    auctions = Auction.objects.select_related('item').all()  # This will retrieve all auctions and their related item data
    return render(request, 'auction/auction_dashboard.html', {'auctions': auctions})


@login_required
def auction_close(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.user == auction.item.vendor.user:
        auction.end_time = timezone.now()
        auction.save()
        # Additional logic to determine the winner, if applicable
    return redirect('auction_dashboard')  # Redirect to the dashboard or another appropriate page


@login_required
def auction_comment(request, auction_id):
    if request.method == 'POST':
        auction = get_object_or_404(Auction, pk=auction_id)
        comment_text = request.POST.get('comment', '')  # Assuming there's a text input named 'comment' in your form
        if comment_text:
            Comment.objects.create(auction=auction, user=request.user, text=comment_text)
            return redirect('auction_detail', auction_id=auction_id)
    return HttpResponse("Method not allowed", status=405)  # Return a 405 Method Not Allowed response


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    auction = Auction.objects.filter(item=item).first()  # Assuming each item has an associated auction
    return render(request, 'auction/item_detail.html', {'item': item, 'auction': auction})

@login_required
def place_bid(request, item_id):
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        item = get_object_or_404(Item, pk=item_id)
        # Implement your logic for placing a bid here
        # Ensure the bid is higher than the starting bid and any existing bids
        return redirect('item_detail', item_id=item_id)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    # Set the price based on bid or direct purchase, here assuming direct purchase
    cart_item.price = item.starting_bid  # or any other logic to set the price
    cart_item.save()
    
    return redirect('cart_detail')  # Redirect to the cart detail page


def cart_detail(request):
    if request.user.is_authenticated:
        # For authenticated users, retrieve or create a cart linked to the user
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
    else:
        # For non-authenticated users, use session to store cart ID
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return render(request, 'auction/auction_cart.html', {'cart': cart})

@login_required
def payment(request):
    form = PaymentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()

            # Create a Stripe PaymentIntent
            stripe.api_key = settings.STRIPE_PRIVATE_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency='usd',
                metadata={'payment_id': payment.id}
            )

            # Redirect to the payment processing view
            return redirect('process_payment', intent.client_secret)

    context = {'form': form}
    return render(request, 'payment.html', context)

def process_payment(request, client_secret):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        intent = stripe.PaymentIntent.confirm(client_secret)

        if intent.status == 'succeeded':
            # Update the Payment model
            payment_id = intent.metadata['payment_id']
            payment = Payment.objects.get(id=payment_id)
            payment.paid = True
            payment.save()

            messages.success(request, 'Payment successful!')
            return redirect('success')

    context = {'client_secret': client_secret}
    return render(request, 'process_payment.html', context)


def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    return render(request, 'auction/auction_detail.html', {'auction': auction})


@login_required
def auction_bid(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    bid_amount = request.POST.get('bid_amount', 0)
    current_highest_bid = item.bid_set.order_by('-bid_amount').first()

    if current_highest_bid is None or bid_amount > current_highest_bid.bid_amount:
        new_bid = Bid.objects.create(item=item, customer=request.user, bid_amount=bid_amount)
        item.purchased_amount = bid_amount
        item.purchased_by = request.user
        item.save()
        # Redirect to item detail or confirmation page
        return HttpResponseRedirect(reverse('item_detail', args=[item_id]))
    else:
        # Handle the case where the bid is not high enough
        pass
    return redirect('auction_detail', auction_id=item_id)