import os

import aiofiles
from fastapi import UploadFile

from app.config.settings import settings
from app.exceptions.base import AppException
from app.core.response import HttpResp

SIZE = 2048


class LocalStorage:
    """
    :path 放到指定文件夹（下级不在分文件夹，主要针对个性业务）
    avatar
    默认分类->每天一个文件夹独立保存上传文件
    image
    video
    file
    """
    @classmethod
    async def upload(cls, file_in: UploadFile, key: str):
        """folder + "/" + date + "/" + uuid + '.' + ext"""
        directory = settings.UPLOAD_DIR
        paths = key.split('/')
        save_name = paths[-1]
        _date = paths[-2]
        folder = '/'.join(paths[:-2])
        save_path = os.path.join(directory, folder, _date).replace('\\', '/')
        file_name = os.path.join(save_path, save_name).replace('\\', '/')

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        try:
            async with aiofiles.open(file_name, 'wb') as file_out:
                content = await file_in.read(SIZE)
                while content:
                    await file_out.write(content)
                    content = await file_in.read(SIZE)
        except Exception as e:
            raise AppException(HttpResp.FAILED, msg='上传文件失败:%s' % e)
