import os

import openai
import requests

headers = {
    "Cookie": "buvid3=624DC525-E7B5-0416-1735-7CD7AF68A3A245957infoc; i-wanna-go-back=-1; _uuid=D812FC103-1B8D-288E-A16A-D395A6581082645694infoc; buvid4=505CDFDF-0FEE-9CD2-F219-129A152C10CA46623-022071123-cWZGbE4cldom6m5ltwQ11A==; buvid_fp_plain=undefined; LIVE_BUVID=AUTO5716575551770605; CURRENT_BLACKGAP=0; DedeUserID=361453208; DedeUserID__ckMd5=4cb1e81e3095816d; nostalgia_conf=-1; blackside_state=0; b_ut=5; is-2022-channel=1; fingerprint3=adff839f4ad592c1c87e6205cb0ef759; hit-dyn-v2=1; b_nut=100; rpdid=|(k|k)~u|mYR0J'uYY)mullYu; CURRENT_QUALITY=120; header_theme_version=CLOSE; home_feed_column=5; CURRENT_FNVAL=4048; CURRENT_PID=d6815990-cf09-11ed-9502-f922cc9137c4; FEED_LIVE_VERSION=V8; browser_resolution=2560-1289; hit-new-style-dyn=0; bsource=search_baidu; fingerprint=606cee3cf376d013849ff9b45826538d; buvid_fp=606cee3cf376d013849ff9b45826538d; PVID=1; SESSDATA=0c4e71ce,1698493717,6baa2*51; bili_jct=b139ffb592d46dbe26ce7dd47ea61ceb; sid=8njneye0; innersign=1; b_lsid=AD31C7DC_187D866137F; bp_video_offset_361453208=790810144955957200"}


def bili_info(bvid):
    params = (
        ('bvid', bvid),
    )
    response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params)
    return response.json()['data']


def bili_tags(bvid):
    params = (
        ('bvid', bvid),
    )

    response = requests.get('https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
    data = response.json()['data']
    if data:
        tags = [x['tag_name'] for x in data]
        if len(tags) > 5:
            tags = tags[:5]
    else:
        tags = []
    return tags


def bili_player_list(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bvid
    response = requests.get(url)
    cid_list = [x['cid'] for x in response.json()['data']]
    title = response.json()['data'][0]['part']
    return cid_list[0], title


def bili_subtitle_list(bvid, cid):
    url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    print(url)
    response = requests.get(url, headers=headers)
    subtitles = response.json()['data']['subtitle']['subtitles']
    if subtitles:
        return ['https:' + x['subtitle_url'] for x in subtitles]
    else:
        return []


def bili_subtitle(bvid, cid):
    subtitles = bili_subtitle_list(bvid, cid)
    print(subtitles)
    if subtitles:
        response = requests.get(subtitles[0])
        if response.status_code == 200:
            body = response.json()['body']
            return body
    return []


def segTranscipt(transcript):
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in
                  enumerate(transcript)]
    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    length = len(text)
    seg_length = 3500
    n = length // seg_length + 1
    print(f"视频文本共{length}字, 分为{n}部分进行摘要")
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt


def chat(text, ):
    prompt = '作为一名专业的视频内容编辑，你的任务是总结以下视频字幕文本的精华内容，并以无序列表的方式返回。请确保所有句子都足够简洁、清晰和完整。 ' \
             '注意，你需要理解并概括原始文本中的主要信息和关键点，并将其转化成易于理解和记忆的形式。' \
             '同时，请确保你所提供的摘要准确反映了原始文本中所述内容。'
    # openai.api_key = os.environ.get("API_KEY")
    openai.api_key = "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"
    completions = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )

    ans = completions.choices[0].message.content
    return ans
