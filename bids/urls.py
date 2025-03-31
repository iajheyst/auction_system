from django.urls import path

from bids.views import AuctionListView, AuctionCreateView, BidCreateView

urlpatterns = [
    path('', AuctionListView.as_view(), name='auction_list'),
    path('create', AuctionCreateView.as_view(), name='auction_create'),
    path('bid/<int:pk>/', BidCreateView.as_view(), name='bid_create'),
]
