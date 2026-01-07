import datetime
import requests

def log_crm_heartbeat():
    """Logs heartbeat message every 5 minutes to /tmp/crm_heartbeat_log.txt"""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"
    
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    # اختياري: اختبار الـ GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"{now} GraphQL endpoint responsive\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{now} GraphQL endpoint not reachable: {e}\n")
