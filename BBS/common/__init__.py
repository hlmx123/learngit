from django.conf import settings

from redis import Redis


rds = Redis(**settings.REDIS)  # 创建全局的 redis 连接实例
