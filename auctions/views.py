from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from .forms import AuctionForm
from .models import User, Auction, Bid, Watchlist, Category, Comment

#Renders the index page with active listings.
def index(request):
    active_listings = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

#Renders the listing details page. Allows authenticated users to place bids and add comments.
def listing_view(request, listing_id):

    try:
        listing = Auction.objects.get(pk=listing_id)
    except Auction.DoesNotExist:
        raise Http404("Listing does not exist")
    
    highest_bid = Bid.objects.filter(listing=listing).order_by("-bid_amount").first()
    total_bids = Bid.objects.filter(listing=listing).count()

    if request.method == "POST":
        if request.user.is_authenticated:
            bid_amount = request.POST.get("bid_amount")
            if bid_amount is not None and bid_amount.strip() != "":
                try:
                    bid_amount = float(bid_amount)
                    if highest_bid is None or bid_amount > highest_bid.bid_amount:
                        bid = Bid.objects.create(listing=listing, bidder=request.user, bid_amount=bid_amount)
                        messages.success(request, "Bid placed successfully!")
                    else:
                        messages.error(request, "Bid amount must be higher than the current highest bid.")
                except ValueError:
                    messages.error(request, "Invalid bid amount.")
            else:
                messages.error(request, "Bid amount is required.")
        else:
            messages.error(request, "You need to be logged in to place a bid.")

        return redirect("listing", listing_id=listing_id)

    # Check if the listing is already in the user's watchlist
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    # Fetch comments associated with the listing
    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "highest_bid": highest_bid,
        "total_bids": total_bids,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments
    })

#Renders the page with auctions created by the current user.
@login_required
def my_auctions(request):

    #Retrive auctions created by the current user
    user_auctions = Auction.objects.filter(creator=request.user)
    return render(request, "auctions/my_auctions.html", {
        "user_auctions": user_auctions
    })

#Renders the page with auctions won by the current user.
@login_required
def won_auctions(request):
    #Retrive auctions won by the current user
    won_auctions = Auction.objects.filter(winner=request.user)
    return render(request, "auctions/won_auctions.html", {
        "won_auctions": won_auctions
    })

#Handles the addition of comments to a listing.
@login_required
def add_comment(request, listing_id):
    # Retrieve the listing associated with the provided ID
    listing = get_object_or_404(Auction, pk=listing_id)

    #Check if the request method is POST
    if request.method == "POST":
        #Get the comment content from the POST data
        content = request.POST.get("content")
        #Create a new comment object
        comment = Comment.objects.create(listing=listing, commenter=request.user, content=content)
        #Add a success message
        messages.success(request, "Your comment has been added successfully!")
        #Redirect back to the listing page after adding comment
        return redirect("listing", listing_id=listing_id)
    
    #If the request method is not POST or if the form is invalid, redirect back to listing page
    return redirect("listing", listing_id=listing_id)

#Adds a listing to the user's watchlist.
@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)
    
    # Check if the listing is already in the user's watchlist
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        # If the listing is already in the watchlist, redirect with a message
        messages.info(request, "This listing is already in your watchlist.")
        return redirect('listing', listing_id=listing_id)
    
    # Redirect back to the listing page with a success message
    messages.success(request, "Listing successfully added to your watchlist.")
    return redirect('listing', listing_id=listing_id)

# Removes a listing from the user's watchlist.
@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)
    
    # Check if the listing is in the user's watchlist
    watchlist_item = get_object_or_404(Watchlist, user=request.user, listing=listing)
    
    # Remove the listing from the user's watchlist
    watchlist_item.delete()
    
    # Redirect back to the listing page with a success message
    messages.success(request, "Listing successfully removed from your watchlist.")
    return redirect('listing', listing_id=listing_id)

#Renders the watchlist page with listings added by the user.
@login_required
def watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

#Renders the watchlist page with listings added by the user.
@login_required
def categories(request):
    category_items = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "category_items": category_items
    })

#Renders a page with items from a certain category
@login_required
def listing_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Auction.objects.filter(category=category, active=True)
    return render(request, "auctions/by_category.html", {
        "listings": listings,
        "category": category
    })

 #Renders the page to create a new listing.
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            # Since 'creator' is excluded from the form fields, set it manually to the current user
            form.instance.creator = request.user
            form.save()
            return redirect('index')
    else:
        form = AuctionForm(initial={'creator': request.user})  # Set initial value for creator field
        form.fields['creator'].widget = forms.HiddenInput()  # Hide the creator field in the form
    return render(request, 'auctions/create.html', {'form': form})

#Closes an active auction.
@login_required
def close_auction(request, listing_id):
    auction = get_object_or_404(Auction, pk=listing_id)
    if request.user == auction.creator:
        if auction.bids.exists():
            highest_bid = auction.bids.order_by("-bid_amount").first()
            auction.winner = highest_bid.bidder
            auction.active = False
            auction.save()
            messages.success(request, "Auction closed successfully.")
        else:
            messages.error(request, "Cannot close auction without any bids.")
    else:
        messages.error(request, "You are not authorized to close this auction.")
    return redirect("listing", listing_id=listing_id)


#Handles user login.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

#Logs out the user.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#Registers a new user.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
