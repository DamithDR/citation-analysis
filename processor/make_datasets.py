import json
import os
import random

from sklearn.model_selection import train_test_split
from tqdm import tqdm


def get_all_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    files = [file for file in files if file.endswith('.json')]
    return files


def categorise_data(alias):
    root = f'dataset/retrieval_raw_data/{alias}'
    files = get_all_files(root)

    print(f'total number of files : {len(files)}')

    no_citation = []
    one_citation = []
    gr1_less_5_citations = []
    gr5_citations = []

    for file in tqdm(files):
        with open(root + '/' + file, 'r', encoding='utf-8') as f:
            case = json.loads(f.read())

        retrieval_object = {'case': case['neutral_citation'], 'citations': [], 'paragraph_citations': []}
        sequence = case['sequence']
        no_of_citations = 0

        for seq_number in sequence:
            paragraph = case['paragraphs'][seq_number]
            if len(paragraph['neutral_citations']) > 0:
                cited_list = paragraph['neutral_citations']
                for citation in cited_list:
                    retrieval_object['citations'].append(citation['citation'])
                    paragraph_linked_citation = {'para': seq_number, 'citation': citation}
                    retrieval_object['paragraph_citations'].append(paragraph_linked_citation)
                    no_of_citations += len(citation['paragraphs'])

        if no_of_citations == 0:
            no_citation.append(retrieval_object)
            continue  # takes too much memory, and we don't need these
        elif no_of_citations == 1:
            one_citation.append(retrieval_object)
        elif no_of_citations <= 5:
            gr1_less_5_citations.append(retrieval_object)
        elif no_of_citations > 5:
            gr5_citations.append(retrieval_object)
    return no_citation,one_citation, gr1_less_5_citations, gr5_citations


def make_document_retrieval_dataset(alias):
    no_citation, one_citation, gr1_less_5_citations, gr5_citations = categorise_data(alias)

    print(f'no citations len : {len(no_citation)}')
    print(f'one citations len : {len(one_citation)}')
    print(f'less than 5 citations len : {len(gr1_less_5_citations)}')
    print(f'greater than 5 citations len : {len(gr5_citations)}')

    test_size = 0.2  # 20% test
    dev_size = 0.1  # 10% dev

    # Split for no_citation
    no_citation_train, no_citation_temp = train_test_split(
        no_citation,
        test_size=(test_size + dev_size),
        random_state=42
    )

    # Further split no_citation_temp into test and dev
    no_citation_test, no_citation_dev = train_test_split(
        no_citation_temp,
        test_size=(dev_size / (test_size + dev_size)),
        random_state=42
    )


    # Split for one_citation
    one_citation_train, one_citation_temp = train_test_split(
        one_citation,
        test_size=(test_size + dev_size),
        random_state=42
    )

    # Further split one_citation_temp into test and dev
    one_citation_test, one_citation_dev = train_test_split(
        one_citation_temp,
        test_size=(dev_size / (test_size + dev_size)),
        random_state=42
    )

    # Split for gr1_less_5_citations
    gr1_less_5_citations_train, gr1_less_5_citations_temp = train_test_split(
        gr1_less_5_citations,
        test_size=(test_size + dev_size),
        random_state=42
    )

    # Further split gr1_less_5_citations_temp into test and dev
    gr1_less_5_citations_test, gr1_less_5_citations_dev = train_test_split(
        gr1_less_5_citations_temp,
        test_size=(dev_size / (test_size + dev_size)),
        random_state=42
    )

    # Split for gr5_citations
    gr5_citations_train, gr5_citations_temp = train_test_split(
        gr5_citations,
        test_size=(test_size + dev_size),
        random_state=42
    )

    # Further split gr5_citations_temp into test and dev
    gr5_citations_test, gr5_citations_dev = train_test_split(
        gr5_citations_temp,
        test_size=(dev_size / (test_size + dev_size)),
        random_state=42
    )

    training_data = no_citation_train + one_citation_train + gr1_less_5_citations_train + gr5_citations_train
    random.shuffle(training_data)
    dev_data = no_citation_dev + one_citation_dev + gr1_less_5_citations_dev + gr5_citations_dev
    random.shuffle(dev_data)
    test_data = no_citation_test + one_citation_test + gr1_less_5_citations_test + gr5_citations_test
    random.shuffle(test_data)

    print(f'Training set size : {len(training_data)}')
    print(f'Dev set size : {len(dev_data)}')
    print(f'Test set size : {len(test_data)}')

    with open(f'dataset/retrieval/{alias}/training.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)
    with open(f'dataset/retrieval/{alias}/dev.json', 'w', encoding='utf-8') as f:
        json.dump(dev_data, f, ensure_ascii=False, indent=4)
    with open(f'dataset/retrieval/{alias}/test.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    make_document_retrieval_dataset('public')
    # make_document_retrieval_dataset('experiment')

    # make_passage_retrieval_dataset('public')
