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

# chapter_1_file = os.path.join(json_folder, "Chapter_1.json")
# if os.path.exists(chapter_1_file):
#     with open(chapter_1_file, "r", encoding="utf-8") as f:
#         chapter_1_data = json.load(f)
# else:
#     chapter_1_data = []

# chapter_1_verses = {verse["verse_number"]: verse for verse in chapter_1_data}

# for row in csv_data:
#     if row["Chapter Number"] != "1":
#         continue

#     csv_verse = row["Verse Number"]
#     if "-" in csv_verse:
#         # Handle ranges
#         start, end = map(int, csv_verse.split("-"))
#         for i, json_verse_num in enumerate(range(start + 1, end + 2), start=start):
#             if 16 <= json_verse_num <= 18 or 21 <= json_verse_num <= 22:
#                 continue  # Skip the specified verses
#             if json_verse_num in chapter_1_verses:
#                 verse_data = chapter_1_verses[json_verse_num]
#                 row["Sanskrit Shloka"] += verse_data.get("text", "").strip() + " "
#                 commentaries = verse_data.get("commentaries", [])
#                 hindi_purport = [
#                     commentary.get("description", "").strip()
#                     for commentary in commentaries
#                     if commentary.get("author_name") == "Swami Chinmayananda"
#                 ]
#                 row["Hindi Purport"] += " ".join(hindi_purport) + " "
#     else:
#         csv_verse_num = int(csv_verse)
#         if 16 <= csv_verse_num + 1 <= 18 or 21 <= csv_verse_num + 1 <= 22:
#             continue
#         if csv_verse_num + 1 in chapter_1_verses:
#             verse_data = chapter_1_verses[csv_verse_num + 1]
#             row["Sanskrit Shloka"] = verse_data.get("text", "").strip()
#             commentaries = verse_data.get("commentaries", [])
#             hindi_purport = [
#                 commentary.get("description", "").strip()
#                 for commentary in commentaries
#                 if commentary.get("author_name") == "Swami Chinmayananda"
#             ]
#             row["Hindi Purport"] = " ".join(hindi_purport)

# with open(csv_file, "w", encoding="utf-8", newline="") as f:
#     fieldnames = csv_data[0].keys()
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(csv_data)

# print(f"CSV file updated successfully: {csv_file}")


import os
import json
import csv

def add_sanskrit_shlok_one(json_folder, csv_file, chapter_number):
    """
    Updates a CSV file by enriching it with data from JSON files in the given folder.

    Args:
        json_folder (str): Path to the folder containing JSON files.
        csv_file (str): Path to the CSV file to update.
        chapter_number (int): Chapter number to process.

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

        # load json data chapter wise
        chapter_file = os.path.join(json_folder, f"Chapter_{chapter_number}.json")
        if os.path.exists(chapter_file):
            with open(chapter_file, "r", encoding="utf-8") as f:
                chapter_data = json.load(f)
        else:
            print(f"JSON file for Chapter {chapter_number} not found.")
            return

        chapter_verses = {verse["verse_number"]: verse for verse in chapter_data}

        # add/update json data to csv
        for row in csv_data:
            if row["Chapter Number"] != str(chapter_number):
                continue

            csv_verse = row["Verse Number"]
            if "-" in csv_verse:
                start, end = map(int, csv_verse.split("-"))
                for json_verse_num in range(start + 1, end + 2):
                    if 16 <= json_verse_num <= 18 or 21 <= json_verse_num <= 22:
                        continue
                    if json_verse_num in chapter_verses:
                        verse_data = chapter_verses[json_verse_num]
                        row["Sanskrit Shloka"] += verse_data.get("text", "").strip() + " "
                        commentaries = verse_data.get("commentaries", [])
                        hindi_purport = [
                            commentary.get("description", "").strip()
                            for commentary in commentaries
                            if commentary.get("author_name") == "Swami Chinmayananda"
                        ]
                        row["Hindi Purport"] += " ".join(hindi_purport) + " "
            else:
                csv_verse_num = int(csv_verse)
                if 16 <= csv_verse_num + 1 <= 18 or 21 <= csv_verse_num + 1 <= 22:
                    continue
                if csv_verse_num + 1 in chapter_verses:
                    verse_data = chapter_verses[csv_verse_num + 1]
                    row["Sanskrit Shloka"] = verse_data.get("text", "").strip()
                    commentaries = verse_data.get("commentaries", [])
                    hindi_purport = [
                        commentary.get("description", "").strip()
                        for commentary in commentaries
                        if commentary.get("author_name") == "Swami Chinmayananda"
                    ]
                    row["Hindi Purport"] = " ".join(hindi_purport)

        # write out to csv output
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = csv_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

        print(f"CSV file updated successfully: {csv_file}")

    except Exception as e:
        print(f"Error occurred: {e}")
