from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from books.models import Trade
from books.forms import TradeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def user_trades(request: HttpRequest, user_id: int) -> HttpResponse:
    trades = Trade.objects.exclude(sender=user_id)
    context = {'trades': trades}
    return render(request, 'trade/trade_detail.html', context)


@login_required(login_url='login')
def trade_create(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    trade_form = TradeForm(request.POST or None)
    if request.method == 'POST':
        if trade_form.is_valid():
            trade = trade_form.save(commit=False)
            trade.sender = request.user
            trade.receiver = trade_form.cleaned_data['to_book'].owner
            trade.save()
            messages.success(
                request,
                ('Ви успішно запропонували книгу на обмін!'),
            )
            return redirect('trade_create')
    else:
        trade_form = TradeForm(user=request.user)
    context = {'trade_form': trade_form}
    return render(request, 'trade/trade.html', context)


@login_required(login_url='login')
def trade_delete(request: HttpRequest, trade_id: int) -> HttpResponseRedirect:
    trade = get_object_or_404(Trade, pk=trade_id)
    if request.user.id == trade.receiver.id:
        trade.status = Trade.StatusChoice.Rejected
        trade.save()
        messages.success(request, ('Ви успішно відмовили в обміні!'))
        return redirect('user_trades', request.user.id)
    else:
        return redirect('user_trades', request.user.id)


@login_required(login_url='login')
def trade_confirm(request, trade_id):
    trade = get_object_or_404(Trade, pk=trade_id)
    if request.user == trade.receiver:
        if trade.status == Trade.StatusChoice.Pending:
            trade.status = Trade.StatusChoice.Accepted
            trade.save()
            messages.success(request, 'Ви успішно підтвердили обмін!')
    return redirect('user_trades', request.user.id)
