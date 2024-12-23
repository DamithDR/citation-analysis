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
    cited_neutral_paras = {}
    cited_neutral_paras_list = []
    total_citation_paragraphs = []
    for file_name in tqdm(json_files):
        with open(file_name, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
            if available_cases.__contains__(data['neutral_citation']):
                with open('duplicate_citations.txt', 'a') as dup:
                    duplicates.append(dup)
                    dup.write(f"duplicate citation: {data['neutral_citation']}\n")
            available_cases.add(data['neutral_citation'])
            sequence = data['sequence']
            tot = 0
            for key in sequence:
                if len(data['paragraphs'][key]['neutral_citations']) != 0:
                    citations_list = data['paragraphs'][key]['neutral_citations']
                    cited_neutral_paras_list.extend(citations_list)
                    for cite in citations_list:
                        neutral_citations.add(cite['citation'])
                        cited_neutral_paras[cite['citation']] = cite['paragraphs']
                        tot += len(cite['paragraphs'])

                other_citations.update(data['paragraphs'][key]['other_citations'])
            total_citation_paragraphs.append(tot)

    print(f'all file available citations : {len(available_cases)}')
    print(f'all neutral citations  : {len(neutral_citations)}')
    print(f'all other citations : {len(other_citations)}')
    print(f'cited neutral paras : {len(cited_neutral_paras)}')
    avail_neutral = available_cases.intersection(neutral_citations)
    print(f'files available neutral citations : {len(avail_neutral)}')
    print(f'total duplicates : {len(duplicates)}')

    avail_para_citations = cited_neutral_paras.keys()
    avail_para_cases = available_cases.intersection(avail_para_citations)
    print(f'files avail_para_cases : {len(avail_para_cases)}')

    total_avail_paras = 0
    for case in avail_para_cases:
        total_avail_paras += len(cited_neutral_paras[case])

    print(f'files avail_paras for retreival : {total_avail_paras}')
