from django.db import models


# Create your models here.
class Learner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    adm_no = models.CharField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.name} - {self.adm_no}"

    class Meta:
        verbose_name = "Learner"
        verbose_name_plural = "Learners"
        ordering = ['adm_no']
        db_table = 'learners'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    subject = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100, unique=True)  # isbn no.

    def __str__(self):
        return f"{self.title} - {self.isbn}"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['isbn']
        db_table = 'books'


class Transactions(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='transactions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    expected_return_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} borrowed {self.book} on {self.created_at.strftime('%Y-%m-%d')}"


    @property
    def total_fine(self):
       if self.return_date and self.expected_return_date and self.return_date> self.expected_return_date:
         amount = (self.return_date - self.expected_return_date).days * 10
         return amount
       return 0

    @property
    def days_overdue(self):
        if self.return_date and self.expected_return_date and self.return_date > self.expected_return_date:
            days = (self.return_date - self.expected_return_date).days
            return days
        return 0



    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        db_table = 'transactions'


class Payment(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    code = models.CharField(max_length=30, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="AWAITING_PAYMENT")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        db_table = 'payments'

    def __str__(self):
        return f"{self.merchant_request_id} - {self.code}"

# make migrations
# ALTER DATABASE `library1_db` CHARACTER SET utf8; (django.db.utils.OperationalError)
# an error that table already exists(drop tables from db then run migrations)
