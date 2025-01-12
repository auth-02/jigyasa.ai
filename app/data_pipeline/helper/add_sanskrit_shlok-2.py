# import os
# import json
# import csv

# json_folder = f"/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/json"
# csv_file = r"/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/bhagvad-gita-data.csv"

# with open(csv_file, "r", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     csv_data = list(reader)

# for row in csv_data:
#     row.setdefault("Sanskrit Shloka", "")
#     row.setdefault("Hindi Purport", "")

# for chapter_num in range(1, 19):
#     json_file = os.path.join(json_folder, f"Chapter_{chapter_num}.json")
#     if not os.path.exists(json_file):
#         continue

#     with open(json_file, "r", encoding="utf-8") as f:
#         chapter_data = json.load(f)

#     for verse in chapter_data:
#         chapter_number = verse.get("chapter_number")
#         verse_number = verse.get("verse_number")
#         sanskrit_text = verse.get("text", "").strip()
#         commentaries = verse.get("commentaries", [])

#         if chapter_number == 1 and verse_number > 28:
#             continue

#         hindi_purport = [
#             commentary.get("description", "").strip()
#             for commentary in commentaries
#             if commentary.get("author_name") == "Swami Chinmayananda"
#         ]
#         hindi_purports = " ".join(hindi_purport)

#         for row in csv_data:
#             if str(row["Chapter Number"]) == str(chapter_number):
#                 csv_verse = row["Verse Number"]

#                 if "-" in csv_verse:
#                     start, end = map(int, csv_verse.split("-"))
#                     if start <= verse_number <= end:
#                         row["Sanskrit Shloka"] += sanskrit_text + " "
#                         row["Hindi Purport"] += hindi_purports + " "
#                 elif str(csv_verse) == str(verse_number):
#                     row["Sanskrit Shloka"] = sanskrit_text
#                     row["Hindi Purport"] = hindi_purports

# with open(csv_file, "w", encoding="utf-8", newline="") as f:
#     fieldnames = csv_data[0].keys()
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerows(csv_data)

# print(f"CSV file updated successfully: {csv_file}")

import os
import json
import csv

def add_sanskrit_shlok_two(json_folder, csv_file):
    """
    Updates a CSV file by enriching it with data from JSON files for all chapters.

    Args:
        json_folder (str): Path to the folder containing JSON files.
        csv_file (str): Path to the CSV file to update.

    Returns:
        None
    """
    
    try:
        
        # handle csv data here
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)

        for row in csv_data:
            row.setdefault("Sanskrit Shloka", "")
            row.setdefault("Hindi Purport", "")

        # process each chapter here
        for chapter_num in range(1, 19):
            json_file = os.path.join(json_folder, f"Chapter_{chapter_num}.json")
            if not os.path.exists(json_file):
                print(f"JSON file for Chapter {chapter_num} not found. Skipping...")
                continue

            with open(json_file, "r", encoding="utf-8") as f:
                chapter_data = json.load(f)

            # add/update csv with json data
            for verse in chapter_data:
                chapter_number = verse.get("chapter_number")
                verse_number = verse.get("verse_number")
                sanskrit_text = verse.get("text", "").strip()
                commentaries = verse.get("commentaries", [])

                if chapter_number == 1 and verse_number > 28:
                    continue

                hindi_purport = [
                    commentary.get("description", "").strip()
                    for commentary in commentaries
                    if commentary.get("author_name") == "Swami Chinmayananda"
                ]
                hindi_purports = " ".join(hindi_purport)

                # match/map csv rows with json verse
                for row in csv_data:
                    if str(row["Chapter Number"]) == str(chapter_number):
                        csv_verse = row["Verse Number"]

                        if "-" in csv_verse:
                            start, end = map(int, csv_verse.split("-"))
                            if start <= verse_number <= end:
                                row["Sanskrit Shloka"] += sanskrit_text + " "
                                row["Hindi Purport"] += hindi_purports + " "
                        elif str(csv_verse) == str(verse_number):
                            row["Sanskrit Shloka"] = sanskrit_text
                            row["Hindi Purport"] = hindi_purports

        # write out csv output
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = csv_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(csv_data)

        print(f"CSV file updated successfully: {csv_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
