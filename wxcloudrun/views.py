import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from wxcloudrun.util import chat

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


def chat1(request):
    data = []

    content = chat("")
    return JsonResponse({'code': 0, 'data': data, "message": content},
                        json_dumps_params={'ensure_ascii': False})
