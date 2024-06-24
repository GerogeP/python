import os.path

from typing_extensions import Final

from app.config.settings import settings


class UrlUtil:
    domain: Final[str] = settings.domain
    upload_prefix: Final[str] = settings.upload_prefix

    @classmethod
    async def to_absolute_url(cls, url: str, engine='') -> str:
        """
        转绝对路径
        转前: /uploads/11.png
        转后: https://127.0.0.1/uploads/11.png
        :param url: 相对路径
        :return:
        """
        if not url:
            return ''
        if url.find('/') != 0:
            url = '/' + url
        if url.startswith('/api/static/'):
            return cls.domain + url
        if not engine:
            # engine = await ConfigUtil.get_val("storage", "default", "local")
            engine = "local"
        if engine == 'local':
            return cls.domain + cls.upload_prefix + url
        # config = await ConfigUtil.get_map("storage", engine)
        # return config.get('domain') + url
        return url

    @classmethod
    async def to_relative_url(cls, url: str, engine=None) -> str:
        """
        转相对路径
        转前: https://127.0.0.1/uploads/11.png
        转后: /uploads/11.png
        :param url:
        :return:
        """
        if not url or not url.startswith('http'):
            return url
        if not engine:
            # engine = await ConfigUtil.get_val('storage', 'default', 'local')
            engine = 'local'
        if engine == 'local':
            return url.replace(UrlUtil.domain, '').replace(os.path.join('/', cls.upload_prefix) + '/', '/')
        # config = await ConfigUtil.get_map('storage', engine)
        config = settings.domain
        if config:
            return url.replace(config, '').replace(os.path.join('/', cls.upload_prefix) + '/', '')
        return url
