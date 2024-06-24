#!./venv/bin/python 
"""API for operating data from sql database.

Filename: iat.py
Author: George Pang
Contact: panglilimcse@139.com
"""

from fastapi import APIRouter, Depends, HTTPException
from app.classes.iat_ws_python3 import Ws_Param


router = APIRouter(prefix="/iat")

@router.get("/")
async def test():
    """Test."""
    return 'test is OK'



@router.get("/url")
def get_url():
    """Read item content.

    Args:
    Returns:
        A url string.
    Raises:
    """

    wsParam = Ws_Param(
            APPID='cf59a587', 
            APISecret='OTMzMDUwYzFhMmZhY2E0OWY2Yjg1OThi',
            APIKey='e64ac534bb799fe2f4b80e9711504cf8',
            AudioFile=r'../classes/iat_pcm_16k.pcm')

    url = wsParam.create_url()

    return url


#@router.get("/url4js")
def get_url4js():
    """Read item content.

    Args:
    Returns:
        A url string.
    Raises:
    """

    wsParam = Ws_Param(
            APPID='cf59a587', 
            APISecret='OTMzMDUwYzFhMmZhY2E0OWY2Yjg1OThi',
            APIKey='e64ac534bb799fe2f4b80e9711504cf8',
            AudioFile=r'../classes/iat_pcm_16k.pcm')

    url = wsParam.create_url4js()

    return url


if __name__ == '__main__':

    print(get_url4js())
