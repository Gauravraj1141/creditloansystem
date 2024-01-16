from django.shortcuts import render
import pandas as pd
from .models import Customer,Loan 


def injest_customer_data():
    data = pd.read_excel('customer_data.xlsx')

    for index, row in data.iterrows():
        customer = Customer(
            first_name=row['First Name'],
            last_name=row['Last Name'],
            age=row['Age'],
            phone_number=row['Phone Number'],
            monthly_salary=row['Monthly Salary'],
            approved_limit=row['Approved Limit'],
            current_debt=None  # You might need to adjust this based on your data
        )
        customer.save()

    return {"status":200}
    

def injest_loan_data():
    data = pd.read_excel('loan_data.xlsx')

    for index, row in data.iterrows():
        print(row['Loan ID'],">>these are loan id")
        loan = Loan(
            loan_id=row['Loan ID'],
            customer_id=row['Customer ID'],
            loan_amount=row['Loan Amount'],
            tenure=row['Tenure'],
            interest_rate=row['Interest Rate'],
            monthly_repayment=row['Monthly payment'],
            emis_paid_on_time=row['EMIs paid on Time'],
            start_date=row['Date of Approval'],
            end_date=row['End Date'],
            
        )
        loan.save()
    print("successfully stored data")
    


def run_background_workers():
    status = injest_customer_data()['status']

    if status == 200:
        injest_loan_data()