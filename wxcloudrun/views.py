import json
import logging
import time

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse

from wxcloudrun.models import BilibiliVideo
from wxcloudrun.util import pack_msg, is_bilibili_link, get_bvId, get_data

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
    xml_str = pack_msg(da, "nihao")
    return HttpResponse(xml_str)


def bili_summary(request):
    reply_info = json.loads(request.body)
    print("reply_info", reply_info)
    if not reply_info or reply_info.get("action"):
        return HttpResponse("该公众号暂时无法提供服务，请稍后再试", )
    blink = reply_info["Content"]
    check = is_bilibili_link(blink)
    if not check:
        return HttpResponse("该公众号暂时无法提供服务，请稍后再试", )
    bvid = get_bvId(blink)

    if BilibiliVideo.objects.filter(bvid=bvid).exists():
        summarized_text = BilibiliVideo.objects.get(bvid=bvid).summarized_text

        xml_str = pack_msg(reply_info, summarized_text)
        print(xml_str)
        return HttpResponse(xml_str, )
    else:
        # 异步任务，处理接收到的消息
        get_data(reply_info)
        return HttpResponse('success')
