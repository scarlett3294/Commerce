from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<int:listing_id>", views.listing_view, name="listing"),
    path("listing/<int:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("listings/category/<int:category_id>", views.listing_by_category, name="listing_by_category" ),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("my_auctions/", views.my_auctions, name="my_auctions"),
    path("won_auctions/", views.won_auctions, name="won_auctions"),
]
