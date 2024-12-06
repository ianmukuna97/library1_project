from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from main.models import Book, Transactions, Learner


# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')


def books_stored(request):
    books = Book.objects.all()
    return render(request,'books_stored.html',{'books' : books})


def books_borrowed(request):
    borrowed = Transactions.objects.all()
    return render(request,'books_borrowed.html', {'materials_borrowed' : borrowed})


def books_fined(request):
    return render(request,'books_fined.html')


def books_provided(request):
    return None


def distribute_book(request, id):
    book = Book.objects.get(pk=id)
    learners = Learner.objects.all()
    if request.method == 'POST':
        learner_id = request.POST['learner_id']
        student: Learner = Learner.objects.get(pk=learner_id)
        expected_return_date = date.today() + timedelta(days=7)
        transaction = Transactions.objects.create(book=book, student=student, expected_return_date=expected_return_date, status='DISTRIBUTED')
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
