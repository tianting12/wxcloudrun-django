from django.db import models


class BilibiliVideo(models.Model):
    CHOICES = (
        ('failed', '总结失败'),
        ('successd', '总结成功'),
        ('running', '正在总结'),
        ('ignore', '忽略')
    )

    bvid = models.CharField(max_length=20, unique=True)
    # 视频 BV 号，使用 CharField 类型，并设置最大长度为 20，唯一不重复

    createtime = models.DateTimeField(auto_now_add=True)
    # 视频创建时间，使用 DateTimeField 类型，并设置 `auto_now_add=True`，表示在创建记录时自动设置为当前时间。

    blink = models.CharField(max_length=500, default="")

    creator = models.CharField(max_length=50)
    # 视频创作者，使用 CharField 类型，并设置最大长度为 50。

    summarized_text = models.TextField()

    status = models.CharField(max_length=50, default="")

    # 视频内容，使用 TextField 类型。
