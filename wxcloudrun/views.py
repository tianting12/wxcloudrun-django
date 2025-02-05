import hashlib
import json
import logging
import time
from xml.etree import ElementTree

from django.shortcuts import render
from django.http import HttpResponse

from wxcloudrun.models import BilibiliVideo
from wxcloudrun.receive import ParseXmlMsg
from wxcloudrun.util import is_bilibili_link, get_bvId, get_data
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

        return HttpResponse(content='验证失败')

    elif request.method == 'POST':

        webData = request.body

        xmlData = ElementTree.fromstring(webData)
        print(ElementTree.tostring(xmlData))
        try:
            if xmlData.find('action').text:
                return HttpResponse("success")
        except:
            pass

        recMsg = ParseXmlMsg(xmlData)
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        if recMsg.MsgType == 'text':
            blink = recMsg.Content
            # 检查是否是blibii链接
            print(blink)
            check = is_bilibili_link(blink)
            if not check:
                content = "请输入b站链接"
                print("回复内容：请输入b站链接")
                replyMsg = TextMsg(toUser, fromUser, content)
                return HttpResponse(content=replyMsg.send())
            bvid = get_bvId(blink)
            print("BVID:", bvid)
            if BilibiliVideo.objects.filter(bvid=bvid, status="success").exists():
                obj = BilibiliVideo.objects.get(bvid=bvid)
                replyMsg = TextMsg(toUser, fromUser, obj.summarized_text)
                print("回复内容：", replyMsg.send())
                return HttpResponse(content=replyMsg.send())
            else:
                # 异步任务，处理接收到的消息
                if BilibiliVideo.objects.filter(bvid=bvid).exists():
                    pass
                else:
                    get_data(recMsg)
                time.sleep(2)
                replyMsg = TextMsg(toUser, fromUser, "后台处理中，请10s后在输入连接查看")
                return HttpResponse(content=replyMsg.send())

        elif recMsg.MsgType == 'image':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            replyMsg = TextMsg(toUser, fromUser, "查询中")
            return HttpResponse(content='dd')


def bili_summary(request):
    pass
    # reply_info = json.loads(request.body)
    # print("reply_info", reply_info)
    # if not reply_info or reply_info.get("action"):
    #     return HttpResponse("success", content_type="application/xml")
    # blink = reply_info["Content"]
    # check = is_bilibili_link(blink)
    # if not check:
    #     return HttpResponse("success", content_type="application/xml")
    # bvid = get_bvId(blink)
    #
    # if BilibiliVideo.objects.filter(bvid=bvid).exists():
    #     summarized_text = BilibiliVideo.objects.get(bvid=bvid).summarized_text
    #     TextMsg(toUser, fromUser, content)
    #     return HttpResponse("success", )
    # else:
    #     # 异步任务，处理接收到的消息
    #     get_data(reply_info)
    #     time.sleep(2)
    #     return HttpResponse('success', content_type="application/xml")
