# import csv

# csv_file1 = r"/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/bhagvad-gita-base.csv"
# csv_file2 = r"/home/atharva/DΞVlove/jigyasa.ai/data/processed/bhagvad-gita/bhagvad-gita-data.csv"

# columns_to_add = []
# with open(csv_file1, "r", encoding="utf-8") as file1:
#     reader = csv.DictReader(file1)
#     for row in reader:
#         columns_to_add.append({
#             "Verse Number": row.get("Verse Number", ""),
#             "English Shloka": row.get("English Shloka", "")
#         })

# updated_rows = []
# with open(csv_file2, "r", encoding="utf-8") as file2:
#     reader = csv.DictReader(file2)

#     fieldnames = [fn for fn in reader.fieldnames if fn not in ["Verse Number", "English Shloka"]]
#     for row in reader:
#         updated_row = {key: value for key, value in row.items() if key in fieldnames}
#         updated_rows.append(updated_row)

# for idx, row in enumerate(updated_rows):
#     if idx < len(columns_to_add):
#         row["Verse Number"] = columns_to_add[idx]["Verse Number"]
#         row["English Shloka"] = columns_to_add[idx]["English Shloka"]
#     else:  # Fill with empty values if csv_file1 runs out of data
#         row["Verse Number"] = ""
#         row["English Shloka"] = ""

# if "Chapter Name" in fieldnames:
#     chapter_name_index = fieldnames.index("Chapter Name")
# else:
#     raise ValueError("The column 'Chapter Name' does not exist in the CSV file.")

# new_fieldnames = (
#     fieldnames[:chapter_name_index + 1] +
#     ["Verse Number", "English Shloka"] +
#     fieldnames[chapter_name_index + 1:]
# )

# with open(csv_file2, "w", encoding="utf-8", newline="") as file2:
#     writer = csv.DictWriter(file2, fieldnames=new_fieldnames)
#     writer.writeheader()

#     for row in updated_rows:
#         # Ensure row follows the new field order
#         reordered_row = {key: row.get(key, "") for key in new_fieldnames}
#         writer.writerow(reordered_row)

# print(f"Updated {csv_file2} successfully with reordered columns.")

import csv

def fix_swap_csv_data(csv_file1, csv_file2):
    """
    Updates csv_file2 by adding 'Verse Number' and 'English Shloka' columns 
    from csv_file1 and reorders the columns accordingly.

    Args:
        csv_file1 (str): Path to the source CSV file containing 'Verse Number' and 'English Shloka'.
        csv_file2 (str): Path to the target CSV file to be updated.
    """
    
    try:
        
        # handle csv_file1 here
        columns_to_add = []
        with open(csv_file1, "r", encoding="utf-8") as file1:
            reader = csv.DictReader(file1)
            for row in reader:
                columns_to_add.append({
                    "Verse Number": row.get("Verse Number", ""),
                    "English Shloka": row.get("English Shloka", "")
                })

        # handle csv_file2 here
        updated_rows = []
        with open(csv_file2, "r", encoding="utf-8") as file2:
            reader = csv.DictReader(file2)

            fieldnames = [fn for fn in reader.fieldnames if fn not in ["Verse Number", "English Shloka"]]
            for row in reader:
                updated_row = {key: value for key, value in row.items() if key in fieldnames}
                updated_rows.append(updated_row)

        # add new columns here
        for idx, row in enumerate(updated_rows):
            if idx < len(columns_to_add):
                row["Verse Number"] = columns_to_add[idx]["Verse Number"]
                row["English Shloka"] = columns_to_add[idx]["English Shloka"]
            else:  # Fill with empty values if csv_file1 runs out of data
                row["Verse Number"] = ""
                row["English Shloka"] = ""

        # reorder columns
        if "Chapter Name" in fieldnames:
            chapter_name_index = fieldnames.index("Chapter Name")
        else:
            raise ValueError("The column 'Chapter Name' does not exist in the CSV file.")

        new_fieldnames = (
            fieldnames[:chapter_name_index + 1] +
            ["Verse Number", "English Shloka"] +
            fieldnames[chapter_name_index + 1:]
        )

        # csv_file2 write out 
        with open(csv_file2, "w", encoding="utf-8", newline="") as file2:
            writer = csv.DictWriter(file2, fieldnames=new_fieldnames)
            writer.writeheader()

            for row in updated_rows:
                # Ensure row follows the new field order
                reordered_row = {key: row.get(key, "") for key in new_fieldnames}
                writer.writerow(reordered_row)

        print(f"Updated {csv_file2} successfully with reordered columns.")

    except Exception as e:
        print(f"Error occurred: {e}")
