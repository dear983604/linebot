from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from numpy import tile


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('NvcdSNno+FJMhr5F0Nv5VJ+mXkg8va8BfCttefd7x4DVVhacvrh5l3olFrbJCBvb08gMbI3e+HTWv+9BCZAOao68R5lDszFQeWYPdWoW6l/YA0pH0o2caQNmITFJdPEfZBqmc3Om7gCEuiOiQc/0mAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e50eadd91f664aef19157ce918624d08')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

'''
def handle_message(event):
    message = LocationSendMessage(
        title='台北車站',
        address='台北車站',
        latitude='25.047058',
        longitude='121.519752'

    )
    line_bot_api.reply_message(event.reply_token, message)

def handle_message(event):
    message = ImageSendMessage(original_content_url='https://drive.google.com/file/d/1mRhI1EII3mQNa0h58TaFOgEBdXD_d8NI/view?usp=sharing',
    preview_image_url='https://drive.google.com/file/d/1mRhI1EII3mQNa0h58TaFOgEBdXD_d8NI/view?usp=sharing' )
    line_bot_api.reply_message(event.reply_token, message)

def handle_message(event):
    message = TextSendMessage(text='重複說:'+event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
'''


def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
