from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    # تهيئة GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query لجلب إجمالي العملاء والطلبات والإيرادات
    query = gql("""
    query {
        totalCustomers: customersCount
        totalOrders: ordersCount
        totalRevenue: ordersSumTotalAmount
    }
    """)

    result = client.execute(query)

    # استخراج البيانات
    customers = result.get('totalCustomers', 0)
    orders = result.get('totalOrders', 0)
    revenue = result.get('totalRevenue', 0)

    # تسجيل التقرير في ملف /tmp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    print("CRM report generated!")