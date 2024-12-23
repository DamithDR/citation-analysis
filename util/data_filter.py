import json

from tqdm import tqdm

from util.file_handle import find_json_files


def load_available_files(alias):
    root_directory = f'{alias}/uk'
    json_files = find_json_files(root_directory)
    # json_files = ['public_annotation/uk/uksc/2024/9.json']  # testing purposes

    print(f'found {len(json_files)} json files')

    available_cases = set()
    duplicates = []

    for file_name in tqdm(json_files):
        with open(file_name, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
            if available_cases.__contains__(data['neutral_citation']):
                duplicates.append(data['neutral_citation'])

            available_cases.add(data['neutral_citation'])

    return available_cases


def filter_files(alias, available_cases):
    root_directory = f'{alias}/uk'
    json_files = find_json_files(root_directory)
    # json_files = ['public_annotation/uk/uksc/2024/9.json']  # testing purposes

    removed_citations = 0
    final_dataset = []
    for file_name in tqdm(json_files):
        with open(file_name, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
            for seq in data['sequence']:
                citations_in_paragraph = data['paragraphs'][seq]['neutral_citations']
                available_citations = []
                for citation in citations_in_paragraph:
                    if citation['citation'] in available_cases:  # only add if this case text exist
                        available_citations.append(citation)
                    else:
                        removed_citations += 1

                data['paragraphs'][seq]['neutral_citations'] = available_citations
        final_dataset.append(data)
    print(f'total removed citations = {removed_citations}')
    save_path = f'dataset/{alias}.json'
    with open(save_path, 'w', encoding='utf-8') as json_file:
        json.dump(final_dataset, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    cases = load_available_files('public_annotation')
    filter_files('public_annotation', cases)
    print('public annotation filter done')
    filter_files('experiment_annotation', cases)
    print('experiment annotation filter done')
