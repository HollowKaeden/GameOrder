from django.shortcuts import render


def order(request):
    template = 'order_page/order.html'
    return render(request, template)
