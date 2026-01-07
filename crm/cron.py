# crm/cron.py

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to /tmp/crm_heartbeat_log.txt
    and queries the GraphQL endpoint to ensure it's responsive.
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/crm_heartbeat_log.txt"

    # سجل الرسالة الأساسية
    with open(log_file, "a") as f:
        f.write(f"{now} CRM is alive\n")

    # إعداد transport للاتصال بـ GraphQL
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True) # schema_from_transport 200 ok when POST

    # تعريف query بسيطة (مثال: hello field)
    query = gql(""" query {hello}""")

    try:
        result = client.execute(query)
        with open(log_file, "a") as f:
            f.write(f"{now} GraphQL endpoint responsive: {result}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{now} GraphQL endpoint not reachable: {e}\n")
#___________________________________
# crm/cron.py

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """
    Executes UpdateLowStockProducts mutation every 12 hours
    and logs updated product names and new stock levels.
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/low_stock_updates_log.txt"

    # إعداد transport للاتصال بـ GraphQL
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            updatedProducts {           #updateLowStockProducts,UpdatedProducts,name,stock are response information from graphql query response
                name
                stock
            }
            message
        }
    }
    """)

    try:
        result = client.execute(mutation)
        with open(log_file, "a") as f:
            for prod in result['updateLowStockProducts']['updatedProducts']:
                f.write(f"{now} Updated {prod['name']} to stock {prod['stock']}\n")
            f.write(f"{now} {result['updateLowStockProducts']['message']}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{now} Failed to update low stock products: {e}\n")
