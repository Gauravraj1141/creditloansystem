from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
from creditloan.apis.views_check_eligibility import check_eligibility_json
import random
from datetime import datetime, timedelta

class ViewLoanDetails(APIView):
    
       

    def get(self,request,loan_id):

        try:
            output_payload = {}
            loan = Loan.objects.filter(loan_id=loan_id)
            loan_detail = LoanSerializer(loan,many=True).data[0]
            output_payload["loan_amount"] = loan_detail['loan_amount']
            output_payload["interest_rate"] = loan_detail['interest_rate']
            output_payload["monthly_installment"] = loan_detail['monthly_repayment']
            output_payload["tenure"] = loan_detail['tenure']
           
            customer_details = Customer.objects.filter(customer_id=loan_detail['customer'])
            customer_details_serializer = CustomerSerializer(customer_details,many=True).data[0]
            customer_dict ={}
            customer_dict["customer_id"]=customer_details_serializer['customer_id']
            customer_dict["first_name"]=customer_details_serializer['first_name']
            customer_dict["last_name"]=customer_details_serializer['last_name']
            customer_dict["age"]=customer_details_serializer['age']
            customer_dict["phone_number"]=customer_details_serializer['phone_number']

            output_payload["customer"] = customer_dict

           
            output_json = dict(zip(["Status","Message","Payload"],
                                [200,"Loan for the customer has been successfully Fetched.",output_payload]))
            
            return Response(output_json)
        
        except Exception as e:
                output_json = dict(zip(["Status","Message","Payload","Exception"],
                                    [500,"Internal Server Error",None,e]))
                return Response(output_json)



