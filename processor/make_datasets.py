import json
from sklearn.model_selection import train_test_split


def make_document_retrieval_dataset():
    exp_data = 'dataset/experiment_annotation.json'
    # pub_data = 'dataset/public_annotation_backup.json'

    # with open(exp_data, 'r', encoding='utf-8') as f:
    #     experiment_data = json.load(f)

    zero_citations = []
    one_citation = []
    gr1_less_5_citations = []
    gr5_citations = []

    with open(exp_data, 'r', encoding='utf-8') as f:
        experiment_data = json.load(f)

        for case in experiment_data:
            retrieval_object = {'case': case['neutral_citation'], 'citations': [], 'paragraph_citations': []}
            sequence = case['sequence']
            no_of_citations = 0

            for seq_number in sequence:
                paragraph = case['paragraphs'][seq_number]
                if len(paragraph['neutral_citations']) > 0:
                    cited_list = paragraph['neutral_citations']
                    for citation in cited_list:
                        retrieval_object['citations'].append(citation['citation'])
                        retrieval_object['paragraph_citations'].append(citation)
                        no_of_citations += len(no_of_citations['paragraphs'])

            if no_of_citations == 0:
                zero_citations.append(retrieval_object)
            elif no_of_citations == 1:
                one_citation.append(retrieval_object)
            elif no_of_citations < 5:
                gr1_less_5_citations.append(retrieval_object)
            elif no_of_citations > 5:
                gr5_citations.append(retrieval_object)

    # divide train,test and dev sets
    # train_test_split(zero_citations, test_size=30)
    # Split proportions
    train_size = 0.7  # 70% train
    test_size = 0.2  # 20% test
    dev_size = 0.1  # 10% dev

    # zero_citations = []
    # one_citation = []
    # gr1_less_5_citations = []
    # gr5_citations = []

    # Split train and temp (test + dev)
    one_citation_train, one_citation_temp, gr1_less_5_citations_train, \
    gr1_less_5_citations_temp, gr5_citations_train, gr5_citations_temp = train_test_split(
        one_citation, gr1_less_5_citations, gr5_citations, test_size=(test_size + dev_size),
        random_state=42
    )

    # Split temp into test and dev
    one_citation_test, one_citation_dev, gr1_less_5_citations_test, \
    gr1_less_5_citations_dev, gr5_citations_test, gr5_citations_dev = train_test_split(
        one_citation_temp, gr1_less_5_citations_temp, gr5_citations_temp,
        test_size=(dev_size / (test_size + dev_size)),
        random_state=42
    )

    print(f'Total | Zero {len(zero_citations)}')
    print(f'Total | One {len(one_citation)}')
    print(f'Total | 1 < C < 5 {len(gr1_less_5_citations)}')
    print(f'Total | C > 5  {len(gr5_citations)}')

    training_data = one_citation_train + gr1_less_5_citations_train + gr5_citations_train
    dev_data = one_citation_dev + gr1_less_5_citations_dev + gr5_citations_dev
    test_data = one_citation_test + gr1_less_5_citations_test + gr5_citations_test

    print(training_data)


if __name__ == '__main__':
    make_document_retrieval_dataset()
