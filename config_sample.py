API_TOKEN = "TOKEN_HERE"
ADMIN_ID = 123456789
# redis
REDIS_DB = 1
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASS = ''
# postgres
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = 'user'
POSTGRES_PASS = ''
POSTGRES_DB = 'dbname'
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# webhook
WEBHOOK_HOST = 'https://yoursite.com'
WEBHOOK_PATH = '/path/to/script/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
# web server settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 3001