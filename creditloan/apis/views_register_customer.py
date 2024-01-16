from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *

class RegisterCustomer(APIView):

    """
        :param request:

        {
            "payload": {
                "first_name" : "gaurav"
                "last_name" : "rajput"
                "age" : 23
                "phone_number" :6395463912
                "monthly_salary" :50000
            }
        }
            
    """

    def post(self,request):
        try:
             
            input_json = request.data

            # calculate approved limit 
            approved_limit = round(36 * input_json['monthly_salary']/100000 ) * 100000

            input_dict = dict(zip(["first_name","last_name","age","phone_number","monthly_salary","approved_limit", "current_debt"],
                                [input_json['first_name'],input_json['last_name'],input_json['age'],input_json['phone_number'],input_json['monthly_salary'],approved_limit]))
            
            serializer_var = CustomerSerializer(data=input_dict)
            if serializer_var.is_valid(raise_exception=True):
                serializer_var.save()
            
            output_payload = serializer_var.data
            
            output_json = dict(zip(["Status","Message","Payload"],
                                [200,"Customer registration completed successfully.",output_payload]))
            
            return Response(output_json)
        
        except Exception as e:
                output_json = dict(zip(["Status","Message","Payload","Exception"],
                                    [500,"Internal Server Error",None,e]))
                return Response(output_json)

