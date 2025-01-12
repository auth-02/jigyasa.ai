import pdfplumber
import csv
import re

def extract_text_from_pdf(file_path, start_page, end_page, output_csv):
    """Extract and process text from a given PDF file within the page range."""
    
    extracted_data = []
    chapter_names = []
    translations = []
    purports = []
    verses = []
    
    with pdfplumber.open(file_path) as pdf:
        full_text = ""
        for page_num in range(start_page-1, end_page):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                full_text += text
        
        chapters = get_chapters(full_text)
        print(f"TOTAL CHAPTERS: {len(chapters)}")
        # print(chapters[1])
        
        # if len(chapters) > 0:
        #         print("FIRST CHAPTER:", chapters[0][:100])
        #         print("LAST CHAPTER:", chapters[-1][:100])

        for chapter_text in chapters:
            sections = get_sections(chapter_text)
            chapter_name = get_chapter_name(chapter_text)
            chapter_names.append(chapter_name)
            print(f"TOTAL SECTIONS IN CHAPTER: {len(sections)}")
            print(f"TOTAL CHAPTER NAMES: {len(chapter_names)}")
            
        #     if len(sections) > 0:
        #         print("FIRST SECTION:", sections[0][:200])
        #         print("LAST SECTION:", sections[-1][:200])
                
            for section in sections:
                translation = get_translation(section)
                translations.append(translation)
                purport = get_purport(section)
                purports.append(purport)
                verse = get_verse_number(section)
                verses.append(verse)
                
            print(f"TOTAL TRANSLATIONS: {len(translations)}")
            print(f"TOTAL PURPORTS: {len(translations)}")
            print(f"TOTAL VERSES NUMBERS: {len(verses)}")
            
        
        print(f"CHAPTER NAMES: {chapter_names}")
        
        print(f"SAMPLE SECTION: {sections[27]}")
        print(f"SAMPLE SECTION: {sections[69]}")
            
        #     extracted_data.extend(process_page_text(chapter_text))
    
    return extracted_data

def get_chapters(full_text):
    """Split the full text into individual chapters based on 'CHAPTER'."""
    
    chapters = full_text.split("CHAPTER")[1:] 
    return [f"CHAPTER {chapter.strip()}\n" for chapter in chapters]

def get_sections(chapter_text):
    """Split the chapter text into individual texts (shlokas) based on 'TEXT'."""
    
    sections = chapter_text.split("TEXT")[1:]
    return [f"TEXT {section.strip()}" for section in sections]

def get_translation(section):
    """Extract text between 'TRANSLATION' and 'PURPORT'."""

    translation_start = section.find("TRANSLATION")
    purport_start = section.find("PURPORT")
    
    if translation_start != -1 and purport_start != -1:
        translation = section[translation_start + len("TRANSLATION"):purport_start].strip()
        return translation
    else:
        return ""

def get_purport(section_text):
    """Extract the purport data from the section text. Assumes one purport per section."""
    
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

def get_chapter_name(chapter_text):
    """Extract the chapter name from the chapter text."""
    
    chapter_start = chapter_text.find("CHAPTER")
    text_start = chapter_text.find("TEXT", chapter_start)
    
    if chapter_start == -1 or text_start == -1:
        return None
    
    chapter_name = chapter_text[chapter_start + len("CHAPTER"):text_start].strip()
    return chapter_name

def get_verse_number(section_text):
    """Extract the verse number from the section text."""
    
    match = re.search(r"TEXT\s+(\d+(-\d+)?)", section_text)
    if match:
        return match.group(1)
    return None

def get_word_meanings(text):
    """Extract word meanings (i.e., 'word—meaning' format) before 'TRANSLATION'."""
    
    text_before_translation = text.split("TRANSLATION")[0]
    
    word_meaning_pattern = r"(\w+[-\w]*)(?:—)([^;]+)"
    
    word_meanings = re.findall(word_meaning_pattern, text_before_translation)
    word_meaning_dict = {meaning[0]: meaning[1].strip() for meaning in word_meanings}
    
    return word_meaning_dict

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
            if len(sanskrit_lines[i].split()) <= 3:
                sanskrit_lines[i] = None
        
        final_sanskrit_shloka = "\n".join([line for line in sanskrit_lines if line is not None])
        
        return final_sanskrit_shloka.strip()
    else:
        return None


file_path = '/home/atharva/DΞVlove/jigyasa.ai/data/raw/Bhagvad-Gita.pdf'
start_page = 59
end_page = 186
output_csv = '/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/ch-1.csv'
extracted_data = extract_text_from_pdf(file_path, start_page, end_page, output_csv)
