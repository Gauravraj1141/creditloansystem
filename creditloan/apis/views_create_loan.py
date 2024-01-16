from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
from creditloan.apis.views_check_eligibility import check_eligibility_json
import random
from datetime import datetime, timedelta

class CreateLoan(APIView):
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
       

    def post(self,request):

        try:
            payload_data = check_eligibility_json(request)
            data = payload_data["Payload"]
            message = payload_data["Message"]
            output_payload = {}

            output_payload['loan_id'] = None
            monthly_installment =None
            
            if data['approval']:

                while True:
                    new_id = random.randint(1000, 9999)
                    if not Loan.objects.filter(loan_id=new_id).exists():
                        loan_id = new_id
                        break

                current_date = datetime.now()

                # Calculate the end date by adding the tenure (in months) to the current date
                end_date = current_date + timedelta(days=data['tenure'] * 30)  

                loan_dict = dict(zip(["loan_id", "customer", "loan_amount", "tenure", "interest_rate", "monthly_repayment", "start_date", "end_date"],
                     [loan_id, data['customer_id'], data['loan_amount'], data['tenure'], data['corrected_interest_rate'],
                      round(data['monthly_installment'],2), current_date.date(), end_date.date()]))

                serializer_var = LoanSerializer(data=loan_dict)
                try:
                    if serializer_var.is_valid(raise_exception=True):
                        serializer_var.save()
                except serializers.ValidationError as e:
                    print(e,">>>validation error")
                
                message = "The loan has been successfully created."
                monthly_installment = monthly_installment
                output_payload["loan_id"] = serializer_var.data['loan_id']
            
            output_payload["customer_id"] = data['customer_id']
            output_payload["loan_approved"] = data['approval']
            output_payload["message"] = message
            output_payload["monthly_installment "] = monthly_installment

           
            output_json = dict(zip(["Status","Message","Payload"],
                                [200,"Loan for the customer has been successfully created.",output_payload]))
            
            return Response(output_json)
        
        except Exception as e:
                output_json = dict(zip(["Status","Message","Payload","Exception"],
                                    [500,"Internal Server Error",None,e]))
                return Response(output_json)


