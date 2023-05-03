import asyncio
import json
import logging
import time

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse

from wxcloudrun.models import BilibiliVideo
from wxcloudrun.util import chat, pack_msg, is_bilibili_link, get_bvId, bili_player_list, bili_subtitle, segTranscipt, \
    get_data

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
    xml_tree = ET.Element('xml')
    ET.SubElement(xml_tree, 'ToUserName').text = 'toUser'
    ET.SubElement(xml_tree, 'FromUserName').text = 'fromUser'
    ET.SubElement(xml_tree, 'CreateTime').text = '1348831860'
    ET.SubElement(xml_tree, 'MsgType').text = 'text'
    ET.SubElement(xml_tree, 'Content').text = 'this is a test'
    ET.SubElement(xml_tree, 'MsgId').text = '1234567890123456'
    ET.SubElement(xml_tree, 'MsgDataId').text = 'xxxx'
    ET.SubElement(xml_tree, 'Idx').text = 'xxxx'

    # 将XML元素树序列化为字符串
    xml_str = ET.tostring(xml_tree)

    # 返回HTTP响应
    return HttpResponse(xml_str, content_type='application/xml')


def bili_summary(request):
    reply_info = json.loads(request.body)
    print("reply_info", reply_info)
    if not reply_info or reply_info.get("action"):
        return JsonResponse({'code': 0, 'data': []},
                            json_dumps_params={'ensure_ascii': False})
    blink = reply_info["Content"]
    check = is_bilibili_link(blink)
    if not check:
        print("pass,url 错误")
    bvid = get_bvId(blink)

    if BilibiliVideo.objects.filter(bvid=bvid).exists():
        summarized_text = BilibiliVideo.objects.get(bvid=bvid).summarized_text

        xml_str = pack_msg(reply_info, summarized_text)

        return HttpResponse(xml_str, content_type='application/xml')
    else:
        # 异步任务，处理接收到的消息
        get_data(reply_info)
        time.sleep(3)
        return HttpResponse('success')
