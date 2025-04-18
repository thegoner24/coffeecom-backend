import requests

BASE_URL = "https://nosy-saba-enclosure-cd2f8430.koyeb.app"

# Test credentials for auth endpoints (must exist in your DB or register first)
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"


def print_result(method, endpoint, status, resp_text):
    print(f"{method} {endpoint} -> {status}")
    if status >= 400:
        print(f"  Response: {resp_text[:200]}")


def main():
    endpoints = [
        ("/health", "GET"),
        ("/api/health", "GET"),
        ("/api/auth/login", "POST"),
        ("/api/products/", "GET"),
        ("/api/products/1", "GET"),
        ("/api/cart/", "GET"),
        ("/api/orders/", "GET"),
        ("/api/debug", "GET"),
        ("/debug/health", "GET"),
        ("/api/debug/health", "GET"),
        ("/debug/users", "GET"),
        ("/api/debug/users", "GET"),
        ("/debug/status", "GET"),
        ("/api/debug/status", "GET"),
        ("/debug/info", "GET"),
        ("/api/debug/info", "GET"),
        ("/dev", "GET"),
        ("/dev/info", "GET"),
        ("/dev/health", "GET"),
        ("/test", "GET"),
        ("/test/health", "GET"),
        ("/test/users", "GET"),
        ("/admin/debug", "GET"),
        ("/admin/info", "GET"),
        ("/admin/users", "GET"),
    ]

    # Try to get JWT token first (if login endpoint exists)
    jwt_token = None
    login_url = BASE_URL + "/api/auth/login"
    try:
        resp = requests.post(login_url, json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
        if resp.status_code == 200 and "access_token" in resp.json():
            jwt_token = resp.json()["access_token"]
            print(f"Obtained JWT token for {TEST_EMAIL}")
        else:
            print(f"Login failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Login error: {e}")

    headers = {}
    if jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"

    for endpoint, method in endpoints:
        url = BASE_URL + endpoint
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers)
            elif method == "POST":
                # Use login payload for /api/auth/login, empty for others
                payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD} if "login" in endpoint else {}
                resp = requests.post(url, json=payload, headers=headers)
            else:
                resp = requests.request(method, url, headers=headers)
            print_result(method, endpoint, resp.status_code, resp.text)
        except Exception as e:
            print(f"{method} {endpoint} -> ERROR: {e}")

if __name__ == "__main__":
    main()
