
#!/usr/bin/env python3

import redis
import requests

rc = redis.Redis()

def get_page(url: str) -> str:
    """ get a page and cache value """
    cached_value = rc.get(f"cached:{url}")
    if cached_value is not None:
        # If the cached value exists, increment the count and return the cached value
        rc.incr(f"count:{url}")
        return cached_value.decode()

    # If the cached value doesn't exist, fetch the page and cache the value
    resp = requests.get(url)
    rc.setex(f"cached:{url}", 10, resp.text)
    rc.set(f"count:{url}", 1)
    return resp.text


if __name__ == "__main__":
    # Test the get_page function
    print(get_page('http://slowwly.robertomurray.co.uk'))

    # Check how many times the URL has been checked
    print(rc.get(f"count:http://slowwly.robertomurray.co.uk").decode())

