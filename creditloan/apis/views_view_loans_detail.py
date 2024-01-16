from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
from creditloan.apis.views_check_eligibility import check_eligibility_json
import random
from datetime import datetime, timedelta

class ViewLoansDetail(APIView):
    
       

    def get(self,request,customer_id):

        try:
            loan = Loan.objects.filter(customer_id=customer_id)
            loan_detail_serializer = LoanSerializer(loan,many=True).data

            loans_list =[] 

            for loan_detail in loan_detail_serializer:
                output_payload = {}
                print(loan_detail,'>>loan details')
                tenure = int(loan_detail['tenure'])
                emis_paid_on_time = int(loan_detail['emis_paid_on_time'])

                output_payload["loan_id"] = loan_detail['loan_id']
                output_payload["loan_amount"] = loan_detail['loan_amount']
                output_payload["interest_rate"] = loan_detail['interest_rate']
                output_payload["monthly_installment"] = loan_detail['monthly_repayment']
                output_payload["tenure"] = loan_detail['tenure']

                # calcualte repayments left 
                installments_left = tenure - emis_paid_on_time
                output_payload["repayments_left"] = installments_left

                loans_list.append(output_payload)


           
           
            output_json = dict(zip(["Status","Message","Payload"],
                                [200,"Fetch all the loan details for the customer has been successfully Fetched.",loans_list]))
            
            return Response(output_json)
        
        except Exception as e:
                output_json = dict(zip(["Status","Message","Payload","Exception"],
                                    [500,"Internal Server Error",None,e]))
                return Response(output_json)



