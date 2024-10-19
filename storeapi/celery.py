from celery import Celery
import os
from django.conf import settings

# Устанавливаем переменную окружения для доступа к настройкам Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storeapi.settings')

app = Celery('storeapi')

# Загружаем настройки из Django, используя namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url=settings.CELERY_BROKER_URL
# Автоматически находит все задачи в приложениях проекта
app.autodiscover_tasks()
