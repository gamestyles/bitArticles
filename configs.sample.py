django_settings: dict = {
    "SECRET_KEY": "django-insecure-^o*p+!@1s^4px#*0q98*5eh_nrmrj7b4bqydxvnavwd$5g%wqp",
    "DEBUG": False,
    "ALLOWED_HOSTS": ["127.0.0.1", "localhost"],
    "CSRF_TRUSTED_ORIGINS": ['http://localhost'],
    "IS_SILK_ENABLED": False,

    # logs
    "LOG_DIR_NAME": 'logs/bitArticles.log',
    "LOGGING_FILE_MAX_BYTES": 1024 * 1024 * 5,
    "LOGGING_FILE_BACKUP_COUNT": 5,
    "LOGGING_LEVEL": "DEBUG",
}

# django-reset-framework related settings
drf: dict = {
    # total number of items in each page returned for get queries
    "PAGE_SIZE": 10,
}

api: dict = {
    "API_VERSION": "v1",
}

db: dict = {
    "POSTGRES_DB_NAME": "bitpin",
    "POSTGRES_DB_USER": "postgres",
    "POSTGRES_DB_PASSWORD": "123456",
    "POSTGRES_DB_HOST": "postgres",  # remember if u run want to run locally set this to: localhost
    "POSTGRES_DB_PORT": "5432",
    "CONN_MAX_AGE": 0,
}

redis_config: dict = {
    "redis_username": "",
    "redis_password": "",
    "redis_host": "redis",  # remember if u run want to run locally set this to: localhost
    "redis_port": "6379"
}
redis_config["redis_url"] = "redis://{}:{}@{}:{}".format(
    redis_config.get('redis_username'),
    redis_config.get('redis_password'),
    redis_config.get('redis_host'),
    redis_config.get('redis_port')
)

celery_confs: dict = {
    "CELERY_BROKER_URL": 'redis://:@redis:6379/0',
    "CELERY_RESULT_BACKEND": 'redis://:@redis:6379/0',

    "CELERY_ACCEPT_CONTENT": ['application/json'],
    "CELERY_TASK_SERIALIZER": 'json',
    "CELERY_RESULT_SERIALIZER": 'json',
    "CELERY_TIMEZONE": 'UTC',

    # log settings for celery
    "CELERY_LOG_DIR_NAME": 'logs/celery.log',
    "CELERY_LOGGING_FILE_MAX_BYTES": 1024 * 1024 * 5,
    "CELERY_LOGGING_FILE_BACKUP_COUNT": 5,
    "CELERY_LOG_LEVEL": 'INFO',
    "CELERY_LOG_PROPAGATE": False
}
