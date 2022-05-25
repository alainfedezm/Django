from datetime import datetime
from http.client import HTTPResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from entries.models import Entry
from entries.apiEntry.serializers import EntrySerializer
from rest_framework import status

from django.shortcuts import get_object_or_404


class EntryListApi(APIView):
    def get(self, request):   
        entries = Entry.objects.all()
        return Response(EntrySerializer(entries, many=True).data)
    
    def post(self,request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    
#For a certain user
class EntryDetailAPI(APIView):
    
    def getUser(self, request,pk):
        #pre: Entry identifier that exists and a correct request  
        #post: a Entry data
        user = get_object_or_404(Entry, pk=pk)
        self.check_object_permissions(request, user)
        return user
    
    def get(self, request, pk):
        #pre: Entry identifier that exists and a correct request
        #post: a Entry data       
        user = self.getUser(request,pk)
        serializer = EntrySerializer(instance=user)
        return Response(serializer.data)
    
    #Modify a ENtry
    def put(self, request, pk):
        #pre: Entry identifier that exists and a correct request
        #post: a Entry data
        user = self.getUser(request,pk)
        serializer = EntrySerializer(instance=user, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        
        else: return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    
    #Delete a Entry
    def delete(self, request, pk):
        #pre: Entry identifier that exists and a correct request     
        user = self.getUser(request,pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)