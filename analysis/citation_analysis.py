import json

from tqdm import tqdm

from util.file_handle import find_json_files

if __name__ == '__main__':
    root_directory = 'public_annotation/uk'
    json_files = find_json_files(root_directory)

    print(f'found {len(json_files)} json files')

    available_cases = set()
    neutral_citations = set()
    other_citations = set()
    duplicates = []
    for file_name in tqdm(json_files):
        with open(file_name, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
            if available_cases.__contains__(data['neutral_citation']):
                with open('duplicate_citations.txt', 'a') as dup:
                    duplicates.append(dup)
                    dup.write(f"duplicate citation: {data['neutral_citation']}\n")
            available_cases.add(data['neutral_citation'])
            sequence = data['sequence']
            for key in sequence:
                neutral_citations.update(data['paragraphs'][key]['neutral_citations'])
                other_citations.update(data['paragraphs'][key]['other_citations'])

    print(f'all file available citations : {len(available_cases)}')
    print(f'all neutral citations  : {len(neutral_citations)}')
    print(f'all other citations : {len(other_citations)}')
    avail_neutral = available_cases.intersection(neutral_citations)
    print(f'files available neutral citations : {len(avail_neutral)}')
    print(f'total duplicates : {len(duplicates)}')
