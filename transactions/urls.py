

from django.urls import path
from .views import DepositMoneyView,WithdrawMoneyView,TransactionReportView,PayLoanView, LoanRequestView,make_transaction

# from .import views
urlpatterns = [
    path('make-transaction/<int:book_id>/', make_transaction, name='make_transaction'),
    #  path('purchase-history/', PurchaseHistoryView.as_view(), name='purchase_history'),
    
    path('diposit', DepositMoneyView.as_view(), name='diposit'),
    path('withdraw', WithdrawMoneyView.as_view(), name='Withdraw'),
    path('transaction_report', TransactionReportView.as_view(), name='transaction_report'),
    path('pay_loan/<int:loan_id>/', PayLoanView.as_view(), name='pay_loan'),
    path('loan_request', LoanRequestView.as_view(), name='loan_request'),
    
]