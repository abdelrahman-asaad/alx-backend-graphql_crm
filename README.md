# CRM Celery Setup

## 1. تثبيت Redis و dependencies
pip install -r requirements.txt
sudo service redis-server start

## 2. تشغيل الميجريشن
python manage.py migrate

## 3. تشغيل Celery worker
celery -A crm worker -l info

## 4. تشغيل Celery Beat
celery -A crm beat -l info

## 5. التحقق من التقارير
cat /tmp/crm_report_log.txt