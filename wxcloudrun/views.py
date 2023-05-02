import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


# def counter(request, _):
#     """
#     获取当前计数
#
#      `` request `` 请求对象
#     """
#
#     rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
#     if request.method == 'GET' or request.method == 'get':
#         rsp = get_count()
#     elif request.method == 'POST' or request.method == 'post':
#         rsp = update_count(request)
#     else:
#         rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
#                            json_dumps_params={'ensure_ascii': False})
#     logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
#     return rsp


# def get_count():
#     """
#     获取当前计数
#     """
#
#     try:
#         data = Counters.objects.get(id=1)
#     except Counters.DoesNotExist:
#         return JsonResponse({'code': 0, 'data': 0},
#                             json_dumps_params={'ensure_ascii': False})
#     return JsonResponse({'code': 0, 'data': data.count},
#                         json_dumps_params={'ensure_ascii': False})


# def update_count(request):
#     """
#     更新计数，自增或者清零
#
#     `` request `` 请求对象
#     """
#
#     logger.info('update_count req: {}'.format(request.body))
#
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#
#     if 'action' not in body:
#         return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
#                             json_dumps_params={'ensure_ascii': False})
#
#     if body['action'] == 'inc':
#         try:
#             data = Counters.objects.get(id=1)
#         except Counters.DoesNotExist:
#             data = Counters()
#         data.id = 1
#         data.count += 1
#         data.save()
#         return JsonResponse({'code': 0, "data": data.count},
#                             json_dumps_params={'ensure_ascii': False})
#     elif body['action'] == 'clear':
#         try:
#             data = Counters.objects.get(id=1)
#             data.delete()
#         except Counters.DoesNotExist:
#             logger.info('record not exist')
#         return JsonResponse({'code': 0, 'data': 0},
#                             json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
#                             json_dumps_params={'ensure_ascii': False})


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
