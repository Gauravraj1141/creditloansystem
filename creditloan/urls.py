from creditloan.apis.views_register_customer import RegisterCustomer
from creditloan.apis.views_check_eligibility import CheckEligibility
from creditloan.apis.views_create_loan import CreateLoan
from creditloan.apis.views_view_loan_details import ViewLoanDetails
from creditloan.apis.views_view_loans_detail import ViewLoansDetail
from django.urls import path,include

urlpatterns = [
    path("register/",RegisterCustomer.as_view()),
    path("check-eligibility/",CheckEligibility.as_view()),
    path("create-loan/",CreateLoan.as_view()),
    path("view-loan/<int:loan_id>/",ViewLoanDetails.as_view(),name="view_loan_details"),
    path("view-loans/<int:customer_id>/",ViewLoansDetail.as_view(),name="view_loans_detail")
]
