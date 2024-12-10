import json
from datetime import date, timedelta

from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from main.models import Book, Transactions, Learner, Payment


# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')


def books_stored(request):
    books = Book.objects.all()
    return render(request,'books_stored.html',{'books' : books})


def books_borrowed(request):
    borrowed = Transactions.objects.all()
    return render(request,'books_borrowed.html', {'books_borrowed' : borrowed})


def books_fined(request):
    transactions = Transactions.objects.all()
    fines = [t for t in transactions if t.total_fine > 0]
    return render(request, 'books_fined.html', {'fines': fines})


def books_provided(request):
    return None


def distribute_book(request, id,):
    book = Book.objects.get(pk=id)
    learners = Learner.objects.all()
    if request.method == 'POST':
        learner_id = request.POST['learner_id']
        learner: Learner = Learner.objects.get(pk=learner_id)
        expected_return_date = date.today() + timedelta(days=7)
        transaction = Transactions.objects.create(book=book, learner=learner, expected_return_date=expected_return_date, status='DISTRIBUTED')
        transaction.save()
        messages.success(request, f'Book {book.title} was distributed')
        return redirect('books_stored')
    return render(request, 'distribute.html', {'book' : book, 'learners' : learners})

def return_book(request, id):
    transaction = get_object_or_404(Transactions, pk=id)
    transaction.return_date = date.today()
    transaction.status = 'RETURNED'
    transaction.save()
    messages.success(request, f'Book {transaction.book.title} was returned')
    if transaction.total_fine > 0:
        messages.warning(request, f'Book {transaction.book.title} has incurred a fine of Ksh.{transaction.total_fine}')
    return redirect('books_stored')


def payment_overdue(request, id):
    transactions = Transactions.objects.get(pk=id)
    total = transactions.total_fine
    phone = transactions.student.phone_number
    cl = MpesaClient()
    phone_number = '0723740215'
    amount = 1
    account_reference = transactions.student.adm_no
    transaction_desc = 'Overdue Fines'
    callback_url = 'https://mature-octopus-causal.ngrok-free.app/handle/payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response.response_code == "0":
        payment = Payment.objects.create(transaction=transaction, merchant_request_id=response.merchant_request_id, checkout_request_id=response.checkout_request_id, amount=amount)
        payment.save()
        messages.success(request, f"Payment was requested successfully")
    return redirect('books_fined')


@csrf_exempt
def callback(request):
    resp = json.loads(request.body)
    data = resp['Body']['stkCallback']
    if data["ResultCode"] == "0":
        merchant_id = data["merchantRequestId"]
        checkout_id = data["checkoutRequestId"]
        code =""
        item = data["CallbackMetadata"]["Item"]
        for i in item:
            name = i["Name"]
            if name == "MpesaReceiptNumber":
                code = i["Value"]
        transaction = Transactions.objects.get(merchant_request_id=merchant_id, checkout_request_id=checkout_id)
        transaction.code = code
        transaction.status = "TRANSACTED SUCCESSFULLY"
        transaction.save()
    return HttpResponse("OK")


def pie_chart(request):
    transactions = Transactions.objects.filter(created_at__year=2024)
    returned = transactions.filter(status='RETURNED').count()
    lost = transactions.filter(status='LOST').count()
    borrowed = transactions.filter(status='BORROWED').count()
    return JsonResponse({
        "title": "Grouped By Status",
        "data": {
            "labels": ["Returned", "Borrowed", "Lost"],
            "datasets": [{
                "data": [returned, lost, borrowed],
                "backgroundColor": ['#4e73df', '#1cc88a', '#36b9cc'],
                "hoverBackgroundColor": ['#2e59d9', '#17a673', '#2c9faf'],
                "hoverBorderColor": "rgba(234, 236, 244, 1)",
            }],
        }
    })


def line_chart(request):
    transactions = Transactions.objects.filter(created_at__year=2024)
    grouped  = transactions.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime("%b"))
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Count",
                "lineTension": 0.3,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)",
                "pointRadius": 3,
                "pointBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointBorderColor": "rgba(78, 115, 223, 1)",
                "pointHoverRadius": 3,
                "pointHoverBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointHoverBorderColor": "rgba(78, 115, 223, 1)",
                "pointHitRadius": 10,
                "pointBorderWidth": 2,
                "data": numbers,
            }],
        },

    })


def bar_chart(request):
    transactions = Transactions.objects.filter(created_at__year=2024)
    grouped = transactions.annotate(month=TruncMonth('created_at')).values('month').annotate(
        count=Count('id')).order_by('month')
    numbers = []
    months = []
    for i in grouped:
        numbers.append(i['count'])
        months.append(i['month'].strftime('%b'))
    print(months)
    return JsonResponse({
        "title": "Transactions Grouped By Month",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Total",
                "backgroundColor": "#4e73df",
                "hoverBackgroundColor": "#2e59d9",
                "borderColor": "#4e73df",
                "data": numbers,
            }],
        },
    })
