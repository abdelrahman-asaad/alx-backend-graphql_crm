#!/bin/bash

# مسار مشروع Django
PROJECT_DIR=/c/Users/Dell/Desktop/airbnp/alx_backend_graphql_crm/alx_backend_graphql

# ملف اللوج
LOG_FILE=/tmp/customer_cleanup_log.txt

# الانتقال لمجلد المشروع
cd $PROJECT_DIR || exit 1

# تنفيذ أمر Django shell
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

qs = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)

count = qs.count()
qs.delete()
print(count)
")

# تسجيل النتيجة في اللوج
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> $LOG_FILE
