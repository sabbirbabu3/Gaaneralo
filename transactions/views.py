from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect,render
from django.http import Http404
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constains import DEPOSIT,LOAN,WITHDRAW,LOAN_PAID
from datetime import datetime
from django.db.models import Sum
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from transactions.forms import (
    DepositForm,
    WithdrawForm,
    LoanRequestForm,
)
from transactions.models import Transaction

# def user_transaction_email(user,subject,template,amount):
     
#         message=render_to_string(template, {
#         'user' : user,
#         'amount' : amount,
#         })
#         send_mail=EmailMultiAlternatives(subject, '',  to= [user.email])
#         send_mail.attach_alternative(message, 'text/html')
#         send_mail.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        # user_transaction_email(self.request.user, "deposit Massage","deposit_mail.html", amount )


        return super().form_valid(form)
    

# for test:
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from books.models import Books
from category.models import CategoryModel
from django.core.exceptions import ObjectDoesNotExist

@login_required
def make_transaction(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    
    # Assuming the book prize is the amount to be deducted from the user's balance
    amount = book.prize
    
    # Check if the user has an associated account
    if not request.user.account:
        messages.error(request, 'You do not have an associated account to make this transaction.')
        return redirect('home')  # Redirect to the home page or any other appropriate page
    
    # Get initial values for the form
    initial = {'transaction_type': WITHDRAW}
    # Set the initial value for the book field
    initial['book'] = book.id
    
    # Ensure that the user has sufficient balance for the transaction
    if request.user.account.balance >= amount:
        # Deduct the amount from the user's balance
        request.user.account.balance -= amount
        request.user.account.save()
        
        # Create a transaction record
        Transaction.objects.create(
            account=request.user.account,
            amount=amount,
            balance_afet_transaction=request.user.account.balance,
            transaction_type=1,  # Assuming 1 represents a purchase transaction
        )
        
        # Additional logic if needed
        
        messages.success(request, f'You have successfully purchased {book.title}.')
    else:
        messages.error(request, 'Insufficient balance to make this transaction.')

    return redirect('home')




#cheak2

# class PurchaseHistoryView(LoginRequiredMixin, ListView):
#     template_name = 'profile.html'
#     model = Transaction
#     context_object_name = 'transactions'

#     def get_queryset(self):
#         # Retrieve transactions for the current user and prefetch related book categories
#         return Transaction.objects.filter(account=self.request.user.account).select_related('account__user').prefetch_related('books__category')










class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAW}
        # Assuming you have the book instance available in the view context
        initial['book'] = self.request.user.title.id  # Set the initial value for the book field
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('prize')
        book_id = form.cleaned_data.get('book')  # Retrieve the selected book ID from the form

        # Ensure that the user has an associated account
        if not self.request.user.account:
            raise Http404("User account not found")

        # Check if the user has sufficient balance to withdraw the amount
        if self.request.user.account.balance >= amount:
            # Deduct the withdrawal amount from the user's account balance
            self.request.user.account.balance -= amount
            self.request.user.account.save(update_fields=['balance'])

            # Associate the withdrawal transaction with the selected book
            # Here you can update the book instance with relevant information if needed
            # For example: book.last_withdrawal_amount = amount
            # Save the book instance after updating any relevant information
            # book.save()

            messages.success(
                self.request,
                f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account '
            )
        else:
            messages.error(
                self.request,
                'Insufficient balance in your account to perform this withdrawal'
            )

        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )
        # user_transaction_email(self.request.user, "Loan Request Massage","loan_request_mail.html", amount )
        return super().form_valid(form)


    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                # Reduce the loan amount from the user's balance
                # 5000, 500 + 5000 = 5500
                # balance = 3000, loan = 5000
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('transactions:loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


