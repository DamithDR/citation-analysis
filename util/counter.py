import os


def count_files(base_path):
    result = {}

    for court in os.listdir(base_path):
        court_path = os.path.join(base_path, court)
        if os.path.isdir(court_path):
            court_count = 0
            court_data = {}
            for division in os.listdir(court_path):
                division_path = os.path.join(court_path, division)
                if os.path.isdir(division_path):
                    division_count = 0
                    for root, _, files in os.walk(division_path):
                        division_count += len(files)
                    court_data[division] = division_count
                    court_count += division_count
            result[court] = {'total': court_count, 'divisions': court_data}
    return result


base_path = r"C:\Users\dolamull\PycharmProjects\citation-analysis\data\uk"  # Adjust this path if necessary
file_counts = count_files(base_path)

# Display the result
for court, data in file_counts.items():
    print(f"Court: {court}")
    print(f"  Total files: {data['total']}")
    for division, count in data['divisions'].items():
        print(f"    Division {division}: {count} files")
