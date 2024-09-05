import re
from pprint import pprint
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def contacts_normalize(data):
    correct_contacts = []
    for row in contacts_list:
        full_name = " ".join(row[:3]).strip()
        parts = full_name.split(" ")
        filtered_parts = [part for part in parts if part]

        while len(filtered_parts) < 3:
            filtered_parts.append('')
        new_row = filtered_parts + row[3:]
        correct_contacts.append(new_row)

    return correct_contacts

def number_norm(contacts_list):
    pattern = r"(8|\+7)\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})([-\s]\(*доб.[-\s](\d+)\)*)*"
    for i, row in enumerate(contacts_list):
        if len(row) < 6:
            continue
        row[5] = re.sub(
            pattern,
            lambda m: f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}" +
                      (f" доб.{m.group(7)}" if m.group(7) else ""),
            row[5]
        )
        contacts_list[i] = row

    return contacts_list

normalized_names = contacts_normalize(contacts_list)

normalized_contacts = number_norm(normalized_names)

result_dict = {}

for item in normalized_contacts:
    key = f"{item[0]} {item[1]}"
    if key not in result_dict:
        result_dict[key] = item
    else:
        for count, i in enumerate(item):
            if result_dict[key][count] == i:
                continue
            else:
                if i:
                    result_dict[key][count] = i

result_list = list(result_dict.values())

pprint(result_list)

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_list)