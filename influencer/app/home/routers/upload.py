# coding:utf-8
from typing import List

from fastapi import APIRouter, UploadFile, Form, Request, Security
from fastapi.params import File

from app.models.upload import Upload as UploadModel
from app.plugins.storage.storage_driver import StorageDriver

router = APIRouter()


@router.post("/upload/file", summary="文件上传")
async def upload_file(file: UploadFile, folder_id: int = Form(0), folder: str = Form(None)):
    """单文件上传"""
    result = await StorageDriver.upload(file, folder)

    creat_file = await UploadModel.create(
        channel=1,
        folder_id=folder_id,
        uid=1,
        type=result['type'],
        storage=result['storage'],
        name=result['name'],
        url=result['url'],
        ext=result['ext'],
        size=result['size']
    )
    return creat_file


# multiple
@router.post("/upload/multiple", summary="多文件上传")
async def upload_multiple(files: List[UploadFile] = File(), folder_id: int = Form(0), folder: str = Form(None)):
    """多文件上传"""
    results = []
    try:
        # 保存上传的文件到本地，并记录信息
        for uploaded_file in files:
            try:
                result = await StorageDriver.upload(uploaded_file, folder)

                creat_file = await UploadModel.create(
                    channel=1,
                    folder_id=folder_id,
                    uid=1,
                    type=result['type'],
                    storage=result['storage'],
                    name=result['name'],
                    url=result['url'],
                    ext=result['ext'],
                    size=result['size']
                )
                results.append({"file_name": uploaded_file.filename, "path": creat_file.url})
            except Exception as e:
                results.append({"file_name": uploaded_file.filename, "status": f"Failed to upload: {str(e)}"})
    finally:
        print(results)
    return results
