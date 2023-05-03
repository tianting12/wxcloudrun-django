import json
import logging
import time

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from wxcloudrun.util import chat, pack_msg, is_bilibili_link, get_bvId, bili_player_list, bili_subtitle, segTranscipt

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


def chat1(request):
    reply_info = json.loads(request.body)
    print("reply_info", reply_info)
    if not reply_info:
        return JsonResponse({'code': 0, 'data': []},
                            json_dumps_params={'ensure_ascii': False})
    blink = reply_info["Content"]
    check = is_bilibili_link(blink)
    if not check:
        print("pass,url 错误")
    bvid = get_bvId(blink)

    cid, title = bili_player_list(bvid)
    transcript_text = bili_subtitle(bvid, cid)
    summarized_text = ''
    if transcript_text:
        print('字幕获取成功')
        seged_text = segTranscipt(transcript_text)
        i = 1
        print(seged_text)
        for entry in seged_text:
            try:
                response = chat(entry)
                print(response)
                print(f'完成第{str(i)}部分摘要')
                print()
                i += 1
            except  Exception as e:
                print('GPT接口摘要失败, 请检查网络连接', e)
                response = '摘要失败'
            summarized_text += '\n' + response
        # insert2notion(token, database_id, bvid, summarized_text)
    else:
        print('字幕获取失败')

    if not summarized_text:
        summarized_text = '总结失败'

    print(summarized_text)

    xml_str = pack_msg(reply_info, summarized_text)

    return HttpResponse(xml_str, content_type='application/xml')
