from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView

from bids.forms import AuctionForm, BidForm
from bids.models import Auction, Bid


class AuctionListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = 'auction_list.html'
    queryset = Auction.objects.all()


class AuctionCreateView(LoginRequiredMixin, CreateView):
    model = Auction
    template_name = 'auction_create.html'
    form_class = AuctionForm
    success_url = reverse_lazy('auction_list')

    def form_valid(self, form):
        if form.is_valid():

            if form.cleaned_data['start_price'] <= 0:
                raise ValidationError('Price must be larger than 0')

            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return redirect(self.success_url)
        return super().form_valid(form)

    def get_initial(self):
        return {
            'end_time': timezone.now() + timedelta(days=1),
        }


class BidCreateView(CreateView):
    model = Bid
    form_class = BidForm
    template_name = 'bid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auction'] = Auction.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        if form.is_valid():

            auction = Auction.objects.get(id=self.kwargs['pk'])

            if auction.end_time < timezone.now():
                raise ValidationError('Date must be in the future')

            if form.cleaned_data['price'] <= auction.current_price():
                raise ValidationError('Bid must be larger than current price')

            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.auction = auction
            obj.save()
            return redirect(self.get_success_url())
        return super().form_valid(form)

    def get_initial(self):
        auction = Auction.objects.get(pk=self.kwargs['pk'])
        return {
            'auction': self.kwargs['pk'],
            'price': round(float(auction.current_price()) + 0.01, 2),
        }

    def get_success_url(self):
        return reverse_lazy('bid_create', kwargs={'pk': self.kwargs['pk']})
