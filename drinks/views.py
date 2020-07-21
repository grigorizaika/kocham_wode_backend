import json

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.conf import settings
from django.shortcuts import render

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .forms import StatisticsParametersForm
from .models import Drink
from .serializers import DrinkSerializer
from users.models import User

class DrinkView(APIView):
    permission_classes = [IsAuthenticated]

    def check_user_has_permissions(self, drink, user):
        return drink.user == user or user.is_staff
    
    def get_drink_by_id(self, id, serialized=True):
        drink = Drink.objects.get(pk=id)

        if serialized:
            drink = DrinkSerializer(drink).data

        return drink

    def get_all_drinks(self, serialized=True):
        all_drinks = Drink.objects.all()

        if serialized:
            all_drinks = DrinkSerializer(all_drinks, many=True).data

        return all_drinks

    def get_my_drinks(self, user, serialized=True):
        drinks = user.get_all_drinks()

        if serialized:
            drinks = DrinkSerializer(drinks, many=True).data

        return drinks

    def get_my_drink_by_id(self, user, drink_id, serialized=True):
        drink = (self
                 .get_my_drinks(user, serialized=False)
                 .get(pk=drink_id))

        if serialized:
            drink = DrinkSerializer(drink).data

        return drink

    def get_my_drinks_by_date(self, user, date, serialized=True):
        drinks = user.get_drinks_by_date(date)

        if serialized:
            drinks = DrinkSerializer(drinks, many=True).data

        return drinks

    def get_my_drinks_by_date_range(self, user, date_start, date_end, serialized=True):
        drinks = user.get_drinks_by_date_range(date_start, date_end)

        if serialized:
            drinks = DrinkSerializer(drinks, many=True).data
        
        return drinks

    def get_drinks_by_user_id(self, user_id, serialized=True):
        drinks = Drink.objects.filter(user=user_id)

        if serialized:
            drinks = DrinkSerializer(drinks, many=True).data
        
        return drinks

    def get_drinks_grouped_by_user(
            self, date=None, date_start=None, date_end=None):

        date_args = {
            arg: datetime.strptime(val, '%Y-%m-%d') 
            for arg, val in locals().items() 
            if arg != 'self'
            and val is not None
        }

        drinks_by_user = Drink.objects.group_all_by_user(**date_args)

        drinks_by_user = {
            user: DrinkSerializer(drinks, many=True).data
            for user, drinks in drinks_by_user.items()
        }

        return drinks_by_user

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='date', in_ = openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter(name='date_start', in_ = openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter(name='date_end', in_ = openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter(name='get_for_all_users', in_ = openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter(name='group_by_user', in_ = openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ])
    def get(self, request, *args, **kwargs):
        """
        """
        date = request.GET.get('date')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        get_for_all_users = request.GET.get('get_for_all_users')
        group_by_user = request.GET.get('group_by_user')
        drink_id = kwargs.get('id')
        user_id = kwargs.get('user_id')
        
        if get_for_all_users:
            
            if not request.user.is_staff:
                response = {'drinks': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            
            if drink_id:
                drink = self.get_drink_by_id(drink_id)
                response = {'drinks': drink}
                return Response(response, status=status.HTTP_200_OK)

            if user_id:
                drinks = self.get_drinks_by_user_id(user_id)
                response = {'drinks': drinks}
                return Response(response, status=status.HTTP_200_OK)

            if group_by_user:
                drinks_by_user = self.get_drinks_grouped_by_user(
                    date, date_start, date_end)
                response = {'drinks_by_user': drinks_by_user}
                return Response(response, status=status.HTTP_200_OK)

            drinks = self.get_all_drinks()

            response = {'drinks': drinks}
            
            return Response(response, status=status.HTTP_200_OK)

        if drink_id:
            try:
                drink = self.get_my_drink_by_id(request.user, drink_id)
                response = {'drink': drink}
                return Response(response, status=status.HTTP_200_OK)

            except Drink.DoesNotExist as dne:
                response = {'drink': dne}
                return Response(response, status=status.HTTP_404_DOES_NOT_EXIST)

        if date:
            date = datetime.strptime(date, '%Y-%m-%d')

            drinks = self.get_my_drinks_by_date(request.user, date)

        elif date_start and date_end:
            date_start = datetime.strptime(date_start, '%Y-%m-%d')
            date_end= datetime.strptime(date_end, '%Y-%m-%d')

            drinks = self.get_my_drinks_by_date_range(
                request.user, date_start, date_end)
        
        else:
            drinks = self.get_my_drinks(request.user)

        response = {'drinks': drinks}

        return Response(response)

        # manual_parameters=[
        #     openapi.Parameter(name='when', in_ = openapi.IN_FORM, type=openapi.TYPE_STRING),
        #     openapi.Parameter(name='vol', in_ = openapi.IN_FORM, type=openapi.TYPE_INTEGER),
        #     openapi.Parameter(name='user', in_ = openapi.IN_FORM, type=openapi.TYPE_INTEGER),
        # ]
    def post(self, request, *args, **kwargs):
        data = request.data.dict()

        if 'user' in data:
            if not (data['user'] == request.user.id or request.user.is_staff):
                response = {'user': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            data['user'] = request.user.id
        
        serializer = DrinkSerializer(data=data)

        if serializer.is_valid():
            new_drink = serializer.save()
            response = {'drink': f'Created drink {new_drink.id}'}
            
            return Response(response)

        else:
            response = {'drink': serializer.errors}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    #TODO: port decorators
    #@required_kwargs(['id'])
    def delete(self, request, *args, **kwargs):
        try:
            drink = self.get_drink_by_id(kwargs['id'], serialized=False)
        except Drink.DoesNotExist as dne:
            if request.user.is_staff:
                    return Response(dne, status=status.HTTP_404_NOT_FOUND)
            else:
                response = {'preferences': 'Permission denied'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        if not self.check_user_has_permissions(drink, request.user):
            response = {'preferences': 'Permission denied'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        drink.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


# Non-API views
# TODO: move to a separate file

def get_drinks_grouped_by_user(
       date=None, date_start=None, date_end=None):

    date_args = {
        arg: datetime.strptime(val, '%Y-%m-%d') 
        for arg, val in locals().items() 
        if arg != 'self'
        and val is not None
        and isinstance(val, str)
    }

    drinks_by_user = Drink.objects.group_all_by_user(
        **date_args, key_attribute='email')

    drinks_by_user = {
        # user: serializers.serialize('json', drinks)
        user: DrinkSerializer(drinks, many=True).data
        for user, drinks in drinks_by_user.items()
    }
    
    return json.dumps(drinks_by_user)

@login_required
@staff_member_required
def user_statistics(request):
    if request.method == 'GET':
        form = StatisticsParametersForm()
        
        statistics = get_drinks_grouped_by_user()

        context = {
            'statistics_parameters_form': form,
            'statistics': statistics,
        }
        
        return render(request, 'statistics.html', context=context)
        
    elif request.method == 'POST':
        form = StatisticsParametersForm(request.POST)

        if form.is_valid():
            
            statistics = get_drinks_grouped_by_user(
                form.cleaned_data.get('date', None),
                form.cleaned_data.get('date_start', None),
                form.cleaned_data.get('date_end', None)
            )

            context = {
                'statistics_parameters_form': form,
                'statistics': statistics
            }
            return render(request, 'statistics.html', context=context)
        else:
            context = {
                'statistics_parameters_form': form,
            }
            return render(request, 'statistics.html', context=context)

    return render(request, 'statistics.html')