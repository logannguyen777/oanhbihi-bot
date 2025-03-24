from enum import Enum

class ChannelEnum(Enum):
    web = "web"
    messenger = "messenger"
    zalo = "zalo"

class RoleEnum(str, Enum):
    admin = "admin"
    superadmin = "superadmin"
    bot = "bot"
    user = "user"
