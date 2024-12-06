from django.contrib import admin

from main.models import Learner, Book, Transactions, Payment


# Register your models here.
admin.site.site_header= 'Library One'
admin.site.site_title= 'Library One Management'

class LearnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'adm_no', 'phone_no']
    search_fields = ['name', 'email', 'adm_no', 'phone_no']
    list_per_page = 25

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'subject', 'isbn']
    search_fields = ['title', 'author', 'year', 'subject', 'isbn']
    list_per_page = 32

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'status', 'expected_return_date']
    search_fields = ['book', 'student', 'status', 'expected_return_date']
    list_per_page = 27

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'code', 'amount', 'status', 'created_at']
    search_fields =  ['transaction', 'code', 'amount', 'status', 'created_at']
    list_per_page = 26

admin.site.register(Learner, LearnerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(Payment, PaymentAdmin)

# admin@yahoo.com