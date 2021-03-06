from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Auction
from .forms import AuctionForm
from products.models import Product
from bids.models import Bid
from accounts.models import UserProfile

@login_required
def all_auctions(request):
    """ Creates a view so only registered users can see the auctions """
    if request.user.is_authenticated:
        auctions = Auction.objects.all()
        
        """ Checks to see if any auctions have finished """
        for auction in auctions:
            if not timezone.now() < auction.end_time:
                auction.status = "Closed"
                auction.save()
            return render(request, "auction.html", {"auctions": auctions})

        return render(request, "auction.html", {"auctions": auctions})
    else:
        messages.error(request, "Im sorry but you need to be logged in")
        return redirect(reverse('index'))
        
    return render(request, "index.html")

@login_required
def del_auction(request):
    """ The Owner can request that the Auction been Cancelled before the Time is alloted"""
    if request.method == "POST":
        product_id = request.POST['product_id']
        auction = Auction.objects.get(product_id=product_id)
        product = Product.objects.get(id=product_id)
        current_auction = Auction.objects.filter(product_id=product_id)
        
        current_auction.delete()
            
        return redirect(reverse('auctions'))
@login_required
def open_auction(request):
    """ Allows a registered user to bid on open auctions """
    """ Thanks to Dehinde - Shogbanmu because I really struggled with this part """
    if request.method == "POST":
            product_id = request.POST['product_id']
            auction = Auction.objects.get(product_id=product_id)
            
            """ Make sure Auction is still Open """
            if timezone.now() < auction.end_time:
                product = Product.objects.get(id=product_id)
                current_bid = Bid.objects.filter(product_id=product_id)
                
                if current_bid:
                    """ If there has been a previous Bid then """
                    print("Route A")
                    bid = current_bid[0]
                    bid.user_id = request.user
                    bid.bid_time = timezone.now()
                    bid.bid_views += 1
                    bid.bid_price += int(request.POST['UpBid'])
                    bid.save()
                    auction.current_price = bid.bid_price
                    auction.bid_number += 1
                    auction.current_bidder = str(bid.user_id)
                    auction.save()
                else:
                    """ If there has not been a previous Bid then """
                    print("Route B")
                    new_bid = Bid()
                    new_bid.product_id = product
                    new_bid.auction_id = auction
                    new_bid.user_id = request.user
                    new_bid.bid_time = timezone.now()
                    new_bid.bid_views += 1
                    new_bid.bid_price += int(request.POST['UpBid'])
                    new_bid.save()
                    auction.current_price = new_bid.bid_price
                    auction.bid_number += 1
                    auction.current_bidder = str(new_bid.user_id)
                    auction.save()
                messages.error(request, "Well done you have placed a bid.")
            else:
                auction.status = "Closed"
                auction.save()
                messages.error(request, "This Auction is closed.")
            
    return redirect(reverse('auctions'))
        

@login_required
def add_auctions(request):
    """ Allows Owner to Open Auctions """
    if request.method == 'POST':
      
        AF = AuctionForm(request.POST)
       
        if AF.is_valid():
            AF.save()
            messages.error(request, "Auction Started!")
            return render(request, "addauctions.html", {'AF': AF})
        else:
            messages.error(request, "Auction Failed!")
    else:
        AF = AuctionForm()
    
    return render(request, "addauctions.html", {'AF': AF})
