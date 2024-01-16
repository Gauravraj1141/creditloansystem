from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
from datetime import datetime


class CheckEligibility(APIView):


    def post(self, request):
        """
            :param request:

            {
                "payload": {
                    "customer_id" :22,
                    "loan_amount" : 5656565.23,
                    "interest_rate" : 23.6,
                    "tenure" : 5
                }
            }
                
        """

        output_json = check_eligibility_json(request)
        return Response(output_json)




def check_eligibility_json(request):
        
        try:
            input_json, output_payload = request.data,{}
            customer_id = input_json['customer_id']
            customer_details = Customer.objects.filter(customer_id=customer_id)
            customer_details_serializer = CustomerSerializer(customer_details,many=True).data[0]
            approved_limit = customer_details_serializer['approved_limit']
            monthly_salary = int(customer_details_serializer['monthly_salary'])

            sum_of_current_loans = 0
            sum_of_current_emis = 0
            loan_details = Loan.objects.filter(customer = customer_id)
            loan_details_serializer = LoanSerializer(loan_details,many=True).data

            past_loans_paid_on_time = 0
            num_loans_taken = 0
            loan_activity_current_year = 0
            loan_approved_volume = 0

            for loans in loan_details_serializer:
                end_date = datetime.strptime(loans['end_date'], '%Y-%m-%d')
                start_date = datetime.strptime(loans['start_date'], '%Y-%m-%d')

                current_date = datetime.now()
                current_year = current_date.year
                current_month = current_date.month

                if end_date.year > current_year or (end_date.year == current_year and end_date.month > current_month):
                    sum_of_current_loans += float(loans['loan_amount'])
                    if end_date.year == current_year and end_date.month == current_month:
                        sum_of_current_emis += float(loans['monthly_repayment'])

                else:
                    past_loans_paid_on_time +=1

                
                # get the number of loans taken in past which can be both paid or unpaid
                if start_date.year < current_year or (start_date.year == current_year and start_date.month < current_month):
                    num_loans_taken +=1
                    loan_approved_volume += float(loans['loan_amount'])

                # get the loan activity current year 
                if start_date.year == current_year :
                    loan_activity_current_year +=1

            # print(past_loans_paid_on_time,num_loans_taken, loan_approved_volume,loan_activity_current_year)
            if sum_of_current_loans > approved_limit:
                credit_score = 0 
                message = "The approved limit has been surpassed."
            elif sum_of_current_emis > monthly_salary/2:
                message = "Your monthly salary is insufficient to cover EMIs."
                credit_score = 0 
            else:
                message = "You are eligible to receive the loan."
                weight_paid_on_time = 0.4
                weight_num_loans = 0.2
                weight_loan_activity = 0.2
                weight_approved_volume = 0.2

                # Normalize values to a scale of 0 to 1 for consistent weighting
                normalized_paid_on_time = past_loans_paid_on_time / 100
                normalized_num_loans = 1 - (num_loans_taken / 10)  # Inverse, assuming max 10 loans
                normalized_loan_activity = loan_activity_current_year / 100
                normalized_approved_volume = loan_approved_volume / 1000000  # Normalize to a scale of 0 to 1 million

                # Calculate credit score as a weighted sum
                credit_score = (
                    normalized_paid_on_time * weight_paid_on_time +
                    normalized_num_loans * weight_num_loans +
                    normalized_loan_activity * weight_loan_activity +
                    normalized_approved_volume * weight_approved_volume
                ) * 100
                
            print(credit_score,'credit_score')

            input_json['approval']=False
            input_json['corrected_interest_rate']=input_json['interest_rate']
            input_json['corrected_interest_rate']=input_json['interest_rate']
            input_json['monthly_installment']=0.0
            

            # now calculate the interest rate based on credit score 
            if credit_score > 50:
                input_json['approval']=True
                input_json['corrected_interest_rate']=input_json['interest_rate']
            
            if 50 > credit_score > 30:
                input_json['approval']=True
                input_json['corrected_interest_rate']=12

            if 30 > credit_score > 10:
                input_json['approval']=True
                input_json['corrected_interest_rate']=16


            # now calculate the monthly payment  formula : EMI= P×r×(1+r)**n/ (1+r)**n-1
            # P is the principal amount (loan amount),
            # r is the monthly interest rate (annual interest rate divided by 12 and multiplied by 0.01 to convert it to a decimal),
            # n is the number of monthly installments or tenure in months.
            loan_amount = input_json['loan_amount']
            interest_rate = input_json['corrected_interest_rate']
            tenure_in_months = input_json['tenure']
            monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure_in_months)
            input_json['monthly_installment']=monthly_installment

            output_payload = input_json
            output_json = dict(zip(["Status","Message","Payload"],
                                [200,message,output_payload]))
            
            return output_json
        
        except Exception as e:
            output_json = dict(zip(["Status","Message","Payload","Exception"],
                                [500,"Internal Server Error",None,e]))
            return output_json


def calculate_monthly_installment(loan_amount, annual_interest_rate, tenure_in_months):
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    
    # Calculate EMI using the formula
    emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**tenure_in_months) / ((1 + monthly_interest_rate)**tenure_in_months - 1)
    
    return emi