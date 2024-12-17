from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GetTwitchChannel
from .models import Channel

# 取得訊息回應表符取得身分組
@api_view(['GET'])
def get_all_channel_data(request):
    all_data= [GetTwitchChannel(channel).data for channel in Channel.objects.all().iterator()]
    return Response(all_data)
