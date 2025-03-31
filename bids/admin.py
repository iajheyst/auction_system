from django.contrib import admin

from bids.models import Auction, Bid

admin.site.register(Auction)
admin.site.register(Bid)
