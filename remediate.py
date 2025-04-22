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
