#!/usr/bin/env python3
"""
Script to query GraphQL endpoint for orders in the last 7 days
and log reminders for customers.
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# إعداد النقل
transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# حساب تاريخ 7 أيام مضت
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# تعريف الاستعلام
query = gql(
    """
    query getRecentOrders($date: DateTime!) {
        orders(filter: {order_date_gte: $date}) {
            id
            customer {
                email
            }
        }
    }
    """
)

# تنفيذ الاستعلام
params = {"date": seven_days_ago}
result = client.execute(query, variable_values=params)

# سجل النتيجة في ملف
log_file = "/tmp/order_reminders_log.txt"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        order_id = order["id"]
        email = order["customer"]["email"]
        f.write(f"{now} - Order ID: {order_id}, Customer Email: {email}\n")

print("Order reminders processed!")