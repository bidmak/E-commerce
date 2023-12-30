from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Comment, Bid

def index(request):
    allCategories = Category.objects.all()
    if request.method == "GET":
        active_listings = Listing.objects.filter(isActive=True)
        return render(request, "auctions/index.html", {
            "listings": reversed(active_listings),
            "categories": allCategories,
            "current_category": "select"
        })
    else:
        search = request.POST.get("search", None)
        if not search:
            category_form = request.POST.get("category", "all")
            form_exist = Category.objects.filter(category_name=category_form).exists()
            if category_form == "all" or not form_exist:
                return HttpResponseRedirect(reverse("auctions:index"))
            else:
                category = Category.objects.get(category_name=category_form)
                active_listings = Listing.objects.filter(isActive=True, category=category)
                return render(request, "auctions/index.html", {
                "listings": reversed(active_listings),
                "categories": allCategories,
                "current_category": category_form
                })   
        else:
            active_listings = Listing.objects.filter(isActive=True, title__icontains = search.strip())
            if not active_listings.exists():
                active_listings = Listing.objects.filter(isActive=True)
                if not active_listings.exists():
                    return HttpResponseRedirect(reverse("auctions:index"))
                else: message = True
            else:
                message = False
            return render(request, "auctions/index.html", {
                "listings": reversed(active_listings),
                "categories": allCategories,
                "search": search,
                "message": message
            }) 

@login_required(login_url="auctions:login")
def createListing(request):
    allCategories = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else: 
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        imageurl = request.POST.get("imageurl", "").strip()
        new_category = request.POST.get("new_category", "").strip().capitalize()
        category = request.POST.get("category", "")
        price = request.POST.get("price", None)

        if not imageurl: imageurl = None
        if new_category: 
            category = new_category
            category_exists = Category.objects.filter(category_name=category).exists()
            if not category_exists:
                save_category = Category(category_name=category)
                save_category.save()
            else: pass  
        elif category == "select" or not Category.objects.filter(category_name=category).exists():
            category = "Unspecified"
            category_exists = Category.objects.filter(category_name=category).exists()
            if not category_exists:
                save_category = Category(category_name=category)
                save_category.save()
            else: pass
            
        
        if not title or not description or not price:
            return render(request, "auctions/create.html", {
                "categories": allCategories,
                "message": "Ensure all necessary fields are entered correctly."
            })
        try:
            price = float(price)
            price = round(price, 2)
        except ValueError:
            return render(request, "auctions/create.html", {
                "categories": allCategories,
                "message": "Invalid input, please enter a number for the price."
            })
    
        currentUser = request.user
        categoryData = Category.objects.get(category_name=category)
        newBid = Bid(price=price, user=currentUser)
        newBid.save()
        newListing = Listing(
            title=title,
            description=description,
            category=categoryData,
            bid=newBid,
            imageUrl=imageurl,
            owner=currentUser
        )

        newListing.save()
        return HttpResponseRedirect(reverse("auctions:index"))

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = reversed(listingData.listingcomment.all())
    is_owner = request.user.username == listingData.owner.username
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "is_owner": is_owner
        })
    else:
        currentUser = request.user
        watchlist = request.POST.get("watchlist", None)
        end_auction = request.POST.get("end_auction", None)
        price = request.POST.get("price", None)
        comment = request.POST.get("comment", "").strip()
        
        if watchlist:
            if watchlist == "add":
                listingData.watchlist.add(currentUser)
                isListingInWatchlist = True
            elif watchlist == "remove":
                listingData.watchlist.remove(currentUser)
                isListingInWatchlist = False
            else: pass
            return render(request, "auctions/listing.html", {
                "listing": listingData,
                "isListingInWatchlist": isListingInWatchlist,
                "allComments": allComments,
                "is_owner": is_owner
            })
        elif end_auction:
            if is_owner:
                listingData.isActive = False
                listingData.save()
                return render(request, "auctions/listing.html", {
                    "listing": listingData,
                    "isListingInWatchlist": isListingInWatchlist,
                    "allComments": allComments,
                    "closed": "Congrats!!! Your auction has been closed",
                    "is_owner": is_owner
                })
            else:
                return HttpResponseRedirect(reverse("auctions:listing",args=(id, )))
        elif price:
            try:
                price = float(price)
                price = round(price, 2)
                if price > listingData.bid.price:
                    newBid = Bid(price=price, user=currentUser)
                    newBid.save()
                    listingData.bid = newBid
                    listingData.save()
                    listingData.userBid.add(currentUser)
                    updated = True
                    message = "Your bid has been added successfully."
                else:
                    updated = False
                    message = "Invalid bid, please enter a higer amount."
                return render(request, "auctions/listing.html", {
                "listing": listingData,
                "isListingInWatchlist": isListingInWatchlist,
                "allComments": allComments,
                "message": message,
                "updated": updated,
                "is_owner": is_owner
                })
            except ValueError: 
                return render(request, "auctions/listing.html", {
                "listing": listingData,
                "isListingInWatchlist": isListingInWatchlist,
                "allComments": allComments,
                "message": "Please enter a valid amount.",
                "updated": False,
                "is_owner": is_owner
                })
        elif comment:
            comment = Comment(author=currentUser,listing=listingData,comment=comment)
            comment.save()
            return HttpResponseRedirect(reverse("auctions:listing",args=(id, )))
        else:
            return HttpResponseRedirect(reverse("auctions:listing",args=(id, )))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url="auctions:login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        confirmation = request.POST.get("confirmation", None)

        if not username or not password or not confirmation:
            return render(request, "auctions/register.html", {
                "message": "Ensure all necessary fields are entered correctly."
            })

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Password does not match, please try again."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken, please try a different username."
            })
        
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions:login")
def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": reversed(listings)
    })

@login_required(login_url="auctions:login")
def userBidding(request):
    currentUser = request.user
    listings = currentUser.user_listings.all()
    return render(request, "auctions/bidding.html",{
        "listings": reversed(listings)
    })
