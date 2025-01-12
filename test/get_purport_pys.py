import re
import json

def process_text(text):
  """
  Processes the given text to extract metadata and purports.

  Args:
    text: The input text containing the book contents.

  Returns:
    A dictionary containing:
      - 'metadata': A list of metadata sections (e.g., "INTRODUCTION TO BOOK I").
      - 'purports': A list of purport sections (e.g., the text under "BOOK I").
  """
  
  try:
    start_index = text.index("INTRODUCTION TO BOOK I")
    end_index = text.index("*** END OF THE PROJECT")
    # return text[start_index:end_index]
    
    section_text = text[start_index:end_index]

    data = []
    introductions = []
    purports = []
    roman_numerals = ['I', 'II', 'III', 'IV']
    book_number = 1

    for i, roman in enumerate(roman_numerals):
        intro_pattern = rf"INTRODUCTION TO BOOK {roman}\s*(.*?)\s*BOOK {roman}"
        intro_match = re.search(intro_pattern, section_text, re.DOTALL)
        introduction = intro_match.group(1).strip() if intro_match else ""
        introductions.append({
            "Chapter Number" : book_number,
            "Introduction" : introduction
        })
        
        # print("/n||===================||/n")
        # print(introduction)

        if i < len(roman_numerals) - 1:
            next_roman = roman_numerals[i + 1]
            purport_pattern = rf"(?:BOOK {roman}\s*.*?){{2}}\s*(.*?)\s*INTRODUCTION TO BOOK {next_roman}"
        else:
            purport_pattern = rf"(?:BOOK {roman}\s*.*?){{2}}\s*(.*?)$" 
        purport_match = re.search(purport_pattern, section_text, re.DOTALL)
        purport = purport_match.group(1).strip() if purport_match else ""
        purports.append({
            "Chapter Number" : book_number,
            "Purport" : purport
        })

        data.append({
            "Introductions": introductions,
            "Purports": purports
        })
        
        book_number = book_number + 1
    return data
  except ValueError:
    return ""

def extract_purport(text):
    """
    Extracts purport sections from the given text, 
    assuming each section starts with a number followed by a period.

    Args:
        text: The input text string.

    Returns:
        A list of tuples, where each tuple contains the section number 
        and the corresponding purport text.
    """

    purport_sections = re.findall(r"(\d+\.)\s*(.*?)((?=\d+\.)|$)", text, re.DOTALL)
    return [(section_number.split(".")[0], purport_text.strip()) for section_number, purport_text, _ in purport_sections]

def save_introductions_to_json(data):
  """
  Saves all introductions for all chapters from the given data to a single JSON file.

  Args:
    data: A list of dictionaries, where each dictionary contains:
      - "Introductions": A list of dictionaries, each with "Chapter Number" and "Introduction".
      - "Purports": A list of dictionaries, each with "Chapter Number" and "Purport".
  """
  
  all_introductions = data[0]["Introductions"]
  with open("data/processed/patanjali-yoga-sutra/json/chapters_introduction.json", "w") as f:
    json.dump(all_introductions, f, indent=2, ensure_ascii=False)

def add_purport_to_files(result):
  """
  Adds a "Purport" field to each verse in the chapter_{chapter_number}.json files.

  Args:
    result: The data containing the purports for each chapter.
  """

  for i in range(0, 4):
    chapter_number = i + 1
    filename = f"data/processed/patanjali-yoga-sutra/json/chapter_{chapter_number}.json"

    with open(filename, "r") as f:
      chapter_data = json.load(f)

    purport_list = extract_purport(result[0]["Purports"][i]['Purport']) 
    # print(purport_list)

    purport_idx = 0
    for verse in chapter_data:
      print(purport_list[purport_idx][0])
      print(verse["Verse Number"])
      if int(verse["Verse Number"]) == int(purport_list[purport_idx][0]):
        print(purport_list[purport_idx][1])
        verse["Purport"] = purport_list[purport_idx][1]
      purport_idx = purport_idx + 1
        

    with open(filename, "w") as f:
      json.dump(chapter_data, f, indent=2, ensure_ascii=False)

with open("data/raw/Patanjali-Yoga-Sutra-Gutenberg.txt", "r") as f:
  text = f.read()

result = process_text(text)
save_introductions_to_json(result) 
add_purport_to_files(result)

# print("Purports:")
# print(result[0]["Purports"][3]['Purport'])

# for i in range(0, 4):
#     purport_list = extract_purport(result[0]["Purports"][i]['Purport'])
#     for verse_number, purport in purport_list:
#         print("-" * 20)
#         print(f"Chapter: {i} Verse {verse_number}:")
#         print("-" * 20)
#         print(purport)
