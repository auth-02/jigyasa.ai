import requests
from bs4 import BeautifulSoup
import json

def extract_text_sections(text):
    """
    Extracts and structures text based on the given format.

    Args:
        text: The input text string.

    Returns:
        A dictionary containing the extracted sections:
            - "Sanskrit Shloka": The original shloka.
            - "Padachchhed": Text after the "पदच्छेद" marker.
            - "Word Meanings": 
                - "Hindi": A list of Hindi word meanings.
                - "English": A list of English word meanings.
            - "Sutra Meaning": 
                - "Hindi": Hindi translation.
                - "Sanskrit": Sanskrit translation (usually the original shloka).
                - "English": English translation.
                - "French": French translation (if present).
                - "German": German translation (if present).
    """

    result = {
        "Chapter Name": "",
        "Chapter Number": "",
        "Verse Number": "",
        "Sanskrit Shloka": "",
        "Padachchhed": "",
        "Purport": "",
        "Word Meanings": {
            "Hindi": [],
            "English": []
        },
        "Sutra Meaning": {
            "Hindi": "",
            "Sanskrit": "",
            "English": "",
            "French": "",
            "German": ""
        },
        "Explanations": {}
    }

    lines = text.strip().splitlines()
    if lines:
        result["Sanskrit Shloka"] = lines[0] + "॥"
        
    start_padcched_index = text.find("पदच्छेद:")
    end_padcched_index = text.rfind("शब्दार्थ / Word Meaning")
            
    if start_padcched_index != -1 and end_padcched_index != -1 and start_padcched_index < end_padcched_index:
        hindi_section = text[start_padcched_index:end_padcched_index].strip()
        # print(hindi_section[len("पदच्छेद:"):].strip())
        result["Padachchhed"] = hindi_section[len("पदच्छेद:"):].strip()

    try:
        start_index = text.find("शब्दार्थ / Word Meaning")
        end_index = text.rfind("सूत्रार्थ / Sutra Meaning")
        
        if start_index != -1 and end_index != -1 and start_index < end_index:
            word_meaning_section = text[start_index:end_index]
            # print(word_meaning_section)
            
            if "Hindi" in word_meaning_section: 

                start_index_hindi = word_meaning_section.find("Hindi")
                end_index_hindi = word_meaning_section.rfind("English")
                if start_index_hindi != -1 and end_index_hindi != -1 and start_index_hindi < end_index_hindi:
                    hindi_section = word_meaning_section[start_index_hindi:end_index_hindi].strip()
                    result["Word Meanings"]["Hindi"] = hindi_section.split("\n")[1:] 

            if "English" in word_meaning_section:

                english_section = word_meaning_section.split("English")[1].strip()
                result["Word Meanings"]["English"] = english_section.split("\n")[1:]

            if not result["Word Meanings"]["Hindi"] and not result["Word Meanings"]["English"]:
                result["Word Meanings"]["Hindi"] = word_meaning_section.split("\n")[1:]
    except IndexError:
        pass

    try:
        sutra_meaning_section = text.split("सूत्रार्थ / Sutra Meaning")[1]
        for line in sutra_meaning_section.splitlines():
            if "Hindi:" in line:
                result["Sutra Meaning"]["Hindi"] = line.split("Hindi:")[1].strip()
            elif "Sanskrit:" in line:
                result["Sutra Meaning"]["Sanskrit"] = line.split("Sanskrit:")[1].strip()
            elif "English:" in line:
                result["Sutra Meaning"]["English"] = line.split("English:")[1].strip()
            elif "French:" in line:
                result["Sutra Meaning"]["French"] = line.split("French:")[1].strip()
            elif "German:" in line:
                result["Sutra Meaning"]["German"] = line.split("German:")[1].strip()
    except IndexError:
        pass

    return result

def get_shloka_data(chapter_number, shloka_number, chapter_name):
    """Fetches data for a specific chapter and shloka from the Patanjali Yoga Sutra website."""
    
    if chapter_number == 1:
        base_url = f"https://patanjaliyogasutra.in/{chapter_name}pada{chapter_number}-{shloka_number}/"
    elif chapter_number == 3 and shloka_number == 28:
        base_url = f"https://patanjaliyogasutra.in/3-28/"
    else:
        base_url = f"https://patanjaliyogasutra.in/{chapter_name}-pada-{chapter_number}-{shloka_number}/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(base_url, headers=headers)
        # print(response.text)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_=['tabs-cont-box', 'tabs-cont-box active']) 
        languages = ['Hindi', 'English', 'Sanskrit', 'French', 'German', 'Yog Kavya']

        chapter = soup.find('div', class_='txt').find('a').text.strip() if soup.find('div', class_='txt') and soup.find('a') else "None"
        text = soup.find('div', class_='txt').find('p').text.strip() if soup.find('div', class_='txt') and soup.find('p') else "None"
        
        extracted_data = extract_text_sections(text)
        extracted_data['Chapter Name'] = chapter.split("\n")[0].split(":")[1].strip()
        extracted_data['Chapter Number'] = chapter_number
        extracted_data['Verse Number'] = shloka_number
        # print(extracted_data)
        
        explanations = {}
        for div, language in zip(divs, languages): 
            paragraphs = div.find_all('p')
            list_items = div.find_all('li')

            explanation_parts = []
            for p in paragraphs:
                explanation_parts.append(p.get_text(separator='\n', strip=True))
            for li in list_items:
                explanation_parts.append(li.get_text(strip=True))

            explanations[language] = explanation_parts
            extracted_data['Explanations'][language] = explanation_parts
        
        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":

    chapter_verses = {
        'samadhi': 51,
        'sadhana': 55,
        'vibhooti': 55,
        'kaivalya': 34
    }
    
    chapter_number = 1
    for chapter_name, max_shlokas in chapter_verses.items():
        data_list = [] 
        for shloka_number in range(1, max_shlokas + 1):
            data = get_shloka_data(chapter_number, shloka_number, chapter_name) 
            if data:
                data_list.append(data) 
                
        print(data_list)

        with open(f"data/processed/patanjali-yoga-sutra/json/chapter_{chapter_number}.json", "w") as outfile:
            json.dump(data_list, outfile, indent=4, ensure_ascii=False)
            
        chapter_number = chapter_number + 1
