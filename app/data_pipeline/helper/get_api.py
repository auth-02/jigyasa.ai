import http.client
import json
import os

output_dir = "data\\processed\\bhagvad-gita\\json"
os.makedirs(output_dir, exist_ok=True)

api_host = "bhagavad-gita3.p.rapidapi.com"
api_key = "99ab01dfe5mshc16369e0b4de303p159d7bjsnf4cda9d1ba26"

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': api_host
}

def fetch_chapter(chapter_number):
    conn = http.client.HTTPSConnection(api_host)
    endpoint = f"/v2/chapters/{chapter_number}/verses/"
    
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    
    decoded_data = data.decode("utf-8")
    return json.loads(decoded_data)

# Loop through all 18 chapters
for chapter_number in range(1, 19):
    print(f"Fetching data for Chapter {chapter_number}...")
    try:
        chapter_data = fetch_chapter(chapter_number)
        
        output_file = os.path.join(output_dir, f"Chapter_{chapter_number}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chapter_data, f, indent=4, ensure_ascii=False)
        
        print(f"Chapter {chapter_number} saved to {output_file}")
    except Exception as e:
        print(f"Failed to fetch or save Chapter {chapter_number}: {e}")
