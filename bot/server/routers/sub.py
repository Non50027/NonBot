from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import CreateLiveTwitch
from .models import LiveTwitch

# 新訂閱
@api_view(['POST'])
def sub(request):
    serializer= CreateLiveTwitch(data= request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "save data OK", 'data': serializer.data}, status= status.HTTP_201_CREATED)
    
    else:
        raise ValidationError(serializer.errors)

# 更新訂閱
@api_view(['PUT'])
def edit(request):
    data= LiveTwitch.objects.get(user_id= request.data['user_id'])
    
    serializer= CreateLiveTwitch(data, data= request.data, partial= True)
    # 確認資料是否有效
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "update data OK"})
    else:
        return Response(serializer.errors, status=400)
    
# 取得訂閱資料 
@api_view(['GET'])
def get_sub(request):
    data= LiveTwitch.objects.get(user_id= request.data['user_id'])
    return Response(CreateLiveTwitch(data).data)

# 取得所有訂閱資料 
@api_view(['GET'])
def get_all_sub(request):
    all_data= [CreateLiveTwitch(sub).data for sub in LiveTwitch.objects.all().iterator()]
    return Response(all_data)