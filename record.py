import requests
import subprocess

# Configuration
m3u_url = "https://ranapkx.site/RANAPK33k/TVD/tvd.m3u"
target_id = "373484"
output_file = "test_recording.mp4"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://ranapkx.site/"}

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
        # Resolve PHP redirect
        session = requests.Session()
        r = session.get(stream_url, headers=headers, stream=True, timeout=15)
        final_stream_url = r.url
        r.close()

        print(f"Recording 1 minute from: {final_stream_url}")
        
        # FFmpeg Capture (60 seconds)
        subprocess.run([
            "ffmpeg", "-y", "-headers", "User-Agent: Mozilla/5.0\r\nReferer: https://ranapkx.site/\r\n",
            "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
            "-i", final_stream_url, "-t", "60", "-c", "copy", "-bsf:a", "aac_adtstoasc", output_file
        ])
        print("Recording finished.")
    else:
        print("Channel ID not found.")
except Exception as e:
    print(f"Error: {e}")
  
