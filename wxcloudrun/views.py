import hashlib
import json
import logging
import time
from xml.etree import ElementTree

from django.http import JsonResponse
from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import HttpResponse

from wxcloudrun.models import BilibiliVideo
from wxcloudrun.receive import ParseXmlMsg
from wxcloudrun.util import pack_msg, is_bilibili_link, get_bvId, get_data, send
from wxcloudrun.replay import TextMsg

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def demo(request):
    replyMsg = TextMsg("gh_937acfb6dd33", "oXaeL5lrrJ9Xc2TDsCQmVkWLh4Tc", "TEXT")
    return HttpResponse(replyMsg.send(), content_type="application/xml")


def my_view(request):
    # 构造XML元素树
    try:
        da = json.loads(request.body)
        return HttpResponse()
    except Exception as e:
        print(e)
        return HttpResponse('')


# Create your views here.
def TencentView(request):
    if request.method == 'GET':
        # 解析参数
        data = request.GET
        # Flask	from flask import request
        # data = request.args
        if len(data) == 0:
            return HttpResponse(content="hello, this is WeChat view")
        signature = data.get(key='signature', default='')
        timestamp = data.get(key='timestamp', default='')
        nonce = data.get(key='nonce', default='')
        echostr = data.get(key='echostr', default='')
        # 请按照公众平台官网\基本配置中信息填写
        token = "xxxxxxxxxxxxxxxxxx"

        list_para = [token, timestamp, nonce]
        list_para.sort()
        list_str = ''.join(list_para).encode('utf-8')

        sha1 = hashlib.sha1()
        sha1.update(list_str)
        # map(sha1.update, list_para)
        # 加密
        hashcode = sha1.hexdigest()

        print("/GET func: hashcode: {0}, signature: {1}".format(hashcode, signature))

        if hashcode == signature:
            return HttpResponse(content=echostr)
        else:
            return HttpResponse(content='验证失败')

    elif request.method == 'POST':

        webData = request.body

        xmlData = ElementTree.fromstring(webData)
        if json.loads(request.body).get("action"):
            return HttpResponse("success", )
        recMsg = ParseXmlMsg(xmlData)
        if recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = 'test'

            replyMsg = TextMsg(toUser, fromUser, content)
            return HttpResponse(content=replyMsg.send())
        elif recMsg.MsgType == 'image':
            print('暂时不做处理')
            return HttpResponse(content='success')


def bili_summary(request):
    reply_info = json.loads(request.body)
    print("reply_info", reply_info)
    if not reply_info or reply_info.get("action"):
        return HttpResponse("success", content_type="application/xml")
    blink = reply_info["Content"]
    check = is_bilibili_link(blink)
    if not check:
        return HttpResponse("success", content_type="application/xml")
    bvid = get_bvId(blink)

    if BilibiliVideo.objects.filter(bvid=bvid).exists():
        summarized_text = BilibiliVideo.objects.get(bvid=bvid).summarized_text
        # replyMsg = TextMsg(reply_info["FromUserName"], reply_info["ToUserName"], summarized_text)
        # return HttpResponse(replyMsg.send(), content_type="application/xml")
        send(reply_info["FromUserName"], summarized_text)
        return HttpResponse("success", )
    else:
        # 异步任务，处理接收到的消息
        get_data(reply_info)
        time.sleep(2)
        return HttpResponse('success', content_type="application/xml")
