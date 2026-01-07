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

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # تعريف query بسيطة (مثال: hello field)
    query = gql(""" query {hello}""")

    try:
        result = client.execute(query)
        with open(log_file, "a") as f:
            f.write(f"{now} GraphQL endpoint responsive: {result}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{now} GraphQL endpoint not reachable: {e}\n")
