from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from mobile.models import Mobiles
from mobilerestframework.serializers import MobileSerializer

#localhost:8080/api/mobiles/


class MobileListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer=MobileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
#localhost:8080/api/mobiles/{id}/

class MobileUpdateDetailDestroyView(APIView):

    def get(self, request,*args, **kwargs):
        id=kwargs.get('pk')
        qs=Mobiles.objects.get(id=id)
        serializer=MobileSerializer(qs)
        return Response(data=serializer.data)
    
    def put(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        mob_obj=Mobiles.objects.get(id=id)
        serializer=MobileSerializer(data=request.data,instance=mob_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def delete(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        Mobiles.objects.get(id=id).delete()

        
        return Response(data={'message':'mobile deleted'})


class MobileViewSetView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    def create(self, request, *args, **kwargs):
        serializer=MobileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    def retrieve(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        qs=Mobiles.objects.get(id=id)
        serializer=MobileSerializer(qs)
        return Response(data=serializer.data)
    
    def update(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        mob_obj=Mobiles.objects.get(id=id)
        serializer=MobileSerializer(data=request.data,instance=mob_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    

    def destroy(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        Mobiles.objects.get(id=id).delete()
        return Response(data={'message':'mobile deleted'})





