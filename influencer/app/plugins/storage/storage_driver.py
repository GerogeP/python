# coding:utf-8
import os.path
from typing import Optional

from fastapi import UploadFile

from app.config.settings import settings
from app.exceptions.base import AppException
from app.core.response import HttpResp
from app.utils.datetime import get_now_str, FORMAT_DATE2
from app.utils.tools import ToolsUtil
from app.utils.urls import UrlUtil
from app.plugins.storage.engine.local import LocalStorage


# from app.plugins.storage.engine.aliyun import AliyunStorage
# from app.plugins.storage.engine.qiniu import QiniuStorage
# from app.plugins.storage.engine.qcloud import QCloudStorage

class StorageDriver(object):
    """
    文件上传总类方便对接本地，云存储
    /业务（文件分类）/年月日/文件
    folder
        1,业务文件夹 avatar，idcard，等
        2,文件分类，image,video,audio,file
        3,文件下日期
    """

    @classmethod
    async def upload(cls, file_in: UploadFile, folder: Optional[str] = None):
        # system_config 查询存储配置
        # engine = await ConfigUtil.get_val("storage", "default", "local")
        engine = "local"
        # 获取文件大小
        file_size = cls.get_file_size(file_in)
        # 获取文件名
        origin_file_name = file_in.filename
        # 文件扩展名
        origin_ext = origin_file_name.split('.')[-1].lower()
        # 检测文件是否符合上传配置 获取 file_type
        file_type = cls.check_file(file_in, file_size)
        # 设置保存名
        key = cls.build_save_name(file_in, file_type, folder)
        # 对应存储设置，上传
        if engine == 'local':
            await LocalStorage.upload(file_in, key)
            key = key.replace('\\', '/')
        # elif engine == 'qiniu':
        #     result = await QiniuStorage().upload_data(key, file_in.file)
        #     key = result['key']
        # elif engine == 'aliyun':
        #     key = await AliyunStorage().upload_data(key, file_in.file)
        # elif engine == 'qcloud':
        #     key = await QCloudStorage().upload_data(key, file_in.file)
        else:
            raise AppException(HttpResp.FAILED, msg="engine:%s 暂未接入, 暂时不支持" % engine)

        result = {
            'file_type': file_type,
            'storage': engine,
            'name': origin_file_name,
            'url': key,
            'ext': origin_ext,
            'size': file_size,
            'path': await UrlUtil.to_absolute_url(key)
        }
        return result

    @classmethod
    def build_save_name(cls, file_in: UploadFile, file_type, folder):
        """
        保存的文件名
        :return:
        """
        file_folder = {10: 'image', 20: 'video', 30: 'audio', 40: 'file'}
        date = get_now_str(FORMAT_DATE2)
        filename = file_in.filename
        ext = filename.split('.')[-1].lower()
        uuid = ToolsUtil.make_uuid()
        if folder:
            return folder + "/" + date + "/" + uuid + '.' + ext
        else:
            return file_folder[file_type] + "/" + date + "/" + uuid + '.' + ext

    @classmethod
    def check_file(cls, file_in: UploadFile, file_size: int) -> int:
        """检测文件类型 10=图片 20=视频，30=音频，40=文件，大小，是否符合限制，并返回file_type"""
        filename = file_in.filename
        ext = filename.split('.')[-1].lower()
        if not ext:
            raise AppException(HttpResp.FAILED, msg='未知的文件类型')

        if ext in settings.UPLOAD_IMAGE_EXT:
            # 图片文件
            file_type = 10
            limit_size = settings.UPLOAD_IMAGE_SIZE
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传图片不能超出限制:%d M' % (limit_size / 1024 / 1024))
        elif ext in settings.UPLOAD_VIDEO_EXT:
            # 视频文件
            file_type = 20
            limit_size = settings.UPLOAD_VIDEO_SIZE
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传视频不能超出限制:%d M' % (limit_size / 1024 / 1024))
        elif ext in settings.UPLOAD_AUDIO_EXT:
            # 音频文件
            file_type = 30
            limit_size = settings.UPLOAD_AUDIO_SIZE
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传音频不能超出限制:%d M' % (limit_size / 1024 / 1024))
        elif ext in settings.UPLOAD_FILE_EXT:
            # 文件
            file_type = 40
            limit_size = settings.UPLOAD_FILE_SIZE
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传文件不能超出限制:%d M' % (limit_size / 1024 / 1024))
        else:
            raise AppException(HttpResp.FAILED, msg='上传文件类型错误')
        return file_type

    @classmethod
    def get_file_size(cls, file_in: UploadFile):
        """获取文件大小"""
        file_in.file.seek(0, os.SEEK_END)
        file_size = file_in.file.tell()
        file_in.file.seek(0, os.SEEK_SET)
        return file_size
