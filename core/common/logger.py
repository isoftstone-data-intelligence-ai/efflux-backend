import logging.config

# 高级日志配置
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # 必须为 False
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        },
        "color": {  # 带颜色的格式器
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "white",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "color",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "app.log",
        },
    },
    "loggers": {
        "": {  # 根日志器
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy": {  # 配置 SQLAlchemy 日志
            "handlers": ["console", "file"],  # 使用与根日志器相同的处理器
            "level": "WARNING",  # SQLAlchemy 日志级别
            "propagate": False,  # 禁止传播到根日志器
        },
        "sqlalchemy.engine.Engine": {  # 配置 sqlalchemy.engine.Engine 日志
            "handlers": ["console", "file"],  # 使用与根日志器相同的处理器
            "level": "WARNING",  # sqlalchemy.engine.Engine 日志级别
            "propagate": False,  # 禁止传播到根日志器
        },
        "uvicorn.access": {  # FastAPI 的访问日志
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# 应用日志配置
logging.config.dictConfig(LOGGING_CONFIG)

# 日志获取函数
def get_logger(name):
    return logging.getLogger(name)

def logger(cls):
    cls.log = get_logger(cls.__name__)
    return cls