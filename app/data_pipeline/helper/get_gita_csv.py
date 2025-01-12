import re
import csv
import pdfplumber

def extract_text_from_pdf(file_path, start_page, end_page, output_csv):
    """Extract and process text from a given PDF file within the page range."""
    
    extracted_data = []
    
    prev_verse = None
    next_verse = None

    with pdfplumber.open(file_path) as pdf:
        full_text = ""
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                full_text += text

        chapters = get_chapters(full_text)
        print(f"TOTAL CHAPTERS: {len(chapters)}")

        for chapter_num, chapter_text in enumerate(chapters, start=1):
            chapter_name = get_chapter_name(chapter_text)
            chapter_number = chapter_num
            sections = get_sections(chapter_text)

            for section in sections:
                verse_number = get_verse_number(section)
                english_shloka = get_english_shloka(section)
                word_meanings = get_word_meanings(section)
                translation = get_translation(section)
                purport = get_purport(section)
                
                if not verse_number:
                    if prev_verse and next_verse:

                        verse_number = f"{prev_verse + 1}-{next_verse - 1}"
                    elif prev_verse:

                        verse_number = prev_verse + 1
                    elif next_verse:

                        verse_number = next_verse - 1

                extracted_data.append({
                    "Chapter Number": chapter_number,
                    "Chapter Name": chapter_name,
                    "Verse Number": verse_number,
                    "English Shloka": english_shloka,
                    "Word Meanings": word_meanings,
                    "Translation": translation,
                    "Purport": purport
                })
                
                prev_verse = int(verse_number.split('-')[0])
                next_verse = prev_verse + 1
                if '-' in verse_number:
                    next_verse = int(verse_number.split('-')[1])

    save_to_csv(extracted_data, output_csv)
    print(f"Data extracted and saved to {output_csv}")

def get_chapters(full_text):
    """Split the full text into individual chapters based on 'CHAPTER'."""
    
    chapters = full_text.split("CHAPTER")[1:]
    return [f"CHAPTER {chapter.strip()}\n" for chapter in chapters]

def get_sections(chapter_text):
    """Split the chapter text into individual texts (shlokas) based on 'TEXT'."""
    
    sections = chapter_text.split("TEXT")[1:]
    return [f"TEXT {section.strip()}" for section in sections]

def get_chapter_name(chapter_text):
    """Extract the chapter name from the chapter text."""
    
    chapter_start = chapter_text.find("CHAPTER")
    text_start = chapter_text.find("TEXT", chapter_start)
    if chapter_start == -1 or text_start == -1:
        return None
    chapter_name = chapter_text[chapter_start + len("CHAPTER"):text_start].strip()
    chapter_name = f"CHAPTER {chapter_name}"
    return chapter_name

def get_verse_number(section_text):
    """Extract the verse number from the section text."""
    
    match = re.search(r"TEXT\s+(\d+(-\d+)?)", section_text)
    if match:
        return match.group(1)
    return None

def get_english_shloka(section_text):
    """Extract the Sanskrit Shloka and exclude the word meanings."""
    
    text_before_translation = section_text.split("TRANSLATION")[0]
    pattern = r"॥\d+॥\n?([^\n]+(?:\n[^\n]+)*)\n+"
    match = re.search(pattern, text_before_translation)
    if match:
        sanskrit_shloka = match.group(1).strip()
        sanskrit_shloka_cleaned = re.sub(r"—.*", "", sanskrit_shloka)
        sanskrit_lines = sanskrit_shloka_cleaned.split("\n")
        for i in range(4, len(sanskrit_lines)):

            word_count = len(sanskrit_lines[i].split())
            if word_count <= 3 or word_count > 6 or ';' in sanskrit_lines[i]:
                sanskrit_lines[i] = None
        final_sanskrit_shloka = "\n".join([line for line in sanskrit_lines if line is not None])
        return final_sanskrit_shloka.strip()
    return None

def get_word_meanings(text):
    """Extract word meanings (i.e., 'word—meaning' format) before 'TRANSLATION'."""
    
    text_before_translation = text.split("TRANSLATION")[0]
    word_meaning_pattern = r"(\w+[-\w]*)(?:—)([^;]+)"
    word_meanings = re.findall(word_meaning_pattern, text_before_translation)
    word_meaning_dict = {meaning[0]: meaning[1].strip() for meaning in word_meanings}
    return word_meaning_dict

def get_translation(section):
    """Extract text between 'TRANSLATION' and 'PURPORT'. If no 'PURPORT' is found, extract until the end of the section."""
    
    translation_start = section.find("TRANSLATION")
    purport_start = section.find("PURPORT")
    
    if translation_start != -1:
        if purport_start != -1:
            translation = section[translation_start + len("TRANSLATION"):purport_start].strip()
        else:
            translation = section[translation_start + len("TRANSLATION"):].strip()
        return translation
    return ""

def get_purport(section_text):
    """Extract the purport data from the section text. If no purport exists, return None or a message."""
    
    purport_start = section_text.find("PURPORT")
    if purport_start == -1:
        return None
    
    text_start = section_text.find("TEXT", purport_start)
    chapter_start = section_text.find("CHAPTER", purport_start)
    
    if text_start != -1 and (chapter_start == -1 or text_start < chapter_start):
        end_pos = text_start
    elif chapter_start != -1:
        end_pos = chapter_start
    else:
        end_pos = len(section_text)
    
    purport = section_text[purport_start + len("PURPORT"):end_pos].strip()
    return purport

def save_to_csv(data, output_csv):
    """Save extracted data to a CSV file."""
    
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Chapter Number", "Chapter Name", "Verse Number", "English Shloka", "Word Meanings", "Translation", "Purport"])
        writer.writeheader()
        writer.writerows(data)
        

extract_text_from_pdf("/home/atharva/DΞVlove/jigyasa.ai/data/raw/Bhagvad-Gita.pdf", start_page=59, end_page=891, output_csv="/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/bhagvad-gita-data.csv")
