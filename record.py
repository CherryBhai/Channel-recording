import requests
import subprocess
import sys

# Configuration
m3u_url = "https://ranapkx.site/RANAPK33k/TVD/tvd.m3u"
target_id = "373484"
output_file = "test_recording.mp4"

# Spoofing a real Android smartphone to bypass datacenter anti-bot blocks
user_agent = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
headers = {"User-Agent": user_agent, "Referer": "https://ranapkx.site/"}

print("Fetching stream...")
try:
    response = requests.get(m3u_url, headers=headers, timeout=20)
    lines = response.text.splitlines()
    
    stream_url = None
    for i, line in enumerate(lines):
        if target_id in line:
            for j in range(i + 1, min(i + 10, len(lines))):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith("#"):
                    stream_url = candidate
                    break
            break

    if stream_url:
        print(f"Original PHP Link: {stream_url}")
        
        # Attempt to resolve the redirect mimicking a real browser
        session = requests.Session()
        r = session.get(stream_url, headers=headers, stream=True, allow_redirects=True, timeout=15)
        final_stream_url = r.url
        
        # Grab the first 100 characters of the server's response to see if it is blocking us
        chunk = next(r.iter_content(chunk_size=100), b"").decode('utf-8', errors='ignore')
        r.close()

        print(f"Final Media Link: {final_stream_url}")
        if final_stream_url.endswith(".php"):
            print("\n--- SERVER WARNING ---")
            print("The link did not redirect. The server might be blocking GitHub Actions.")
            print(f"Server replied with: {chunk}\n----------------------\n")
        
        print("Starting 1-minute FFmpeg capture...")
        
        # FFmpeg Capture (Forcing User-Agent directly in FFmpeg as well)
        cmd = [
            "ffmpeg", "-y", 
            "-user_agent", user_agent,
            "-headers", "Referer: https://ranapkx.site/\r\n",
            "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
            "-i", final_stream_url, 
            "-t", "60", 
            "-c", "copy", 
            output_file
        ]
        
        subprocess.run(cmd)
        print("Recording finished.")
    else:
        print("Channel ID not found.")
except Exception as e:
    print(f"Error: {e}")
        
