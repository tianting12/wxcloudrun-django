import json
import logging
import time

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse

from wxcloudrun.models import BilibiliVideo
from wxcloudrun.util import pack_msg, is_bilibili_link, get_bvId, get_data
from wxcloudrun.replay import TextMsg

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def demo(request):
    da = json.loads(request.body)
    print(da)
    data = []

    return JsonResponse({'code': 0, 'data': data},
                        json_dumps_params={'ensure_ascii': False})


def my_view(request):
    # 构造XML元素树
    da = json.loads(request.body)
    print(da)
    replyMsg = TextMsg(da["FromUserName"], da["ToUserName"], "TEXT")
    return HttpResponse(replyMsg.send())


def bili_summary(request):
    reply_info = json.loads(request.body)
    print("reply_info", reply_info)
    if not reply_info or reply_info.get("action"):
        return HttpResponse("success")
    blink = reply_info["Content"]
    check = is_bilibili_link(blink)
    if not check:
        return HttpResponse("success")
    bvid = get_bvId(blink)

    if BilibiliVideo.objects.filter(bvid=bvid).exists():
        summarized_text = BilibiliVideo.objects.get(bvid=bvid).summarized_text

        replyMsg = TextMsg(reply_info["FromUserName"], reply_info["ToUserName"], summarized_text)
        return HttpResponse(replyMsg.send())
    else:
        # 异步任务，处理接收到的消息
        get_data(reply_info)
        time.sleep(2)
        return HttpResponse('success')
