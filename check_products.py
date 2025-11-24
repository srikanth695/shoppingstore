import requests, sys
try:
    r = requests.get("http://127.0.0.1:5000/products", timeout=5)
    print("status:", r.status_code)
    print("content-type:", r.headers.get("content-type"))
    print("body:", r.text[:1000])
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)