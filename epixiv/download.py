import os
from hoshino import aiorequests
from . import util

setting = util.get_config().setting

# 下载网络图片到本地
async def get_img(url, save_dir='img', cache=True, headers=None):
    file_name = os.path.basename(url)
    save_dir = util.get_path('data', save_dir)
    path = os.path.join(save_dir, file_name)
    res_path = ('file:///%s' % path)
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)

    if cache and os.path.exists(path):
        if not os.path.getsize(path) == 204:
            return res_path
    proxy = {}
    if setting.proxy_enable:
        proxy = {
            "http": setting.proxy_url,
            "https": setting.proxy_url
        }
    try:
        content = await aiorequests.get(url, timeout=30, headers=headers, proxies=proxy)
        content = await content.content
    except aiorequests.exceptions.ConnectionError:
        return False
    if len(content) == 204:  # 404页面
        return False

    with open(path, 'wb')as fp:
        fp.write(content)

    return res_path
