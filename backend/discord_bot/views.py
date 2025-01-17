import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import CreateLiveTwitch, GetTwitchSub, SerializerRoleMessageEmoji
from .models import LiveTwitch, RoleMessageEmoji
from twitch_bot.models import Channel

# # 新訂閱
# @api_view(['POST'])
# def sub(request):
#     serializer= CreateLiveTwitch(data= request.data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status= status.HTTP_201_CREATED)
    
#     else:
#         raise ValidationError(serializer.errors)

# # 更新訂閱
# @api_view(['PUT'])
# def edit(request):
#     data= LiveTwitch.objects.get(user_id= request.data['user_id'])
    
#     serializer= CreateLiveTwitch(data, data= request.data, partial= True)
#     # 確認資料是否有效
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': "update data OK"})
#     else:
#         return Response(serializer.errors, status=400)
    
# # 取得訂閱資料 
# @api_view(['GET'])
# def get_sub(request):
#     twitch_channel= Channel.objects.get(id= request.data['id'])
#     data= LiveTwitch.objects.get(twitch_channel= twitch_channel)
#     return Response(GetTwitchSub(data).data)

# # 取得所有訂閱資料 
# @api_view(['GET'])
# def get_all_sub(request):
#     all_data= [GetTwitchSub(sub).data for sub in LiveTwitch.objects.all().iterator()]
#     return Response(all_data)

# 設定訊息回應表符取得身分組
@api_view(['POST'])
def set_role_message_emoji(request):
    
    serializer= SerializerRoleMessageEmoji(data= request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
    else:
        raise ValidationError(serializer.errors)
    
# 取得訊息回應表符取得身分組
@api_view(['GET'])
def get_role_message_emoji(request):
    all_data= [SerializerRoleMessageEmoji(sub).data for sub in RoleMessageEmoji.objects.all().iterator()]
    return Response(all_data)
