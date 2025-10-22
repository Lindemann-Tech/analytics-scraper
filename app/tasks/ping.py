"""
Program Name: ping.py
Author: Kevin Lindemann
Date: 10/13/2025
Purpose: Record the time it takes to send an HTTP request to a site. The 'Ping' class is an object which requires a URL to be constructed. The URL will be pulled from an HTML form the user fills out. 
"""

import time, requests

class Ping:
    def __init__(self, url: str):
        self.url = url
    
    def run(self):
        start = time.time()
        try: 
            resp = requests.get(self.url, timeout=15)
            ping_time = round(time.time() - start, 3)
            print(f"Ping to {self.url} responded in {ping_time} with {resp.status_code}")
            return ping_time
        except requests.RequestException as e:
            print(f"""
            Ping Error in app/tasks/ping.py 
            Error: {e}
            """)
            return -1