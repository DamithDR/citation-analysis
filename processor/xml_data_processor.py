import concurrent.futures
import json
import os
from concurrent.futures import as_completed
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

from processor.custom_xml_parser import extract_data
from util.file_handle import find_xml_files


def pre_process(main):
    for table in main.find_all("table"):
        table.decompose()
    return main


def save_annotations(without_text_object, path_split, alias):
    path_split[0] = alias
    file_path = '/'.join(path_split[:len(path_split) - 1])
    if not os.path.exists(file_path):
        path = Path(file_path)
        path.mkdir(parents=True, exist_ok=True)
    file_path = '/'.join(path_split)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(without_text_object, json_file, ensure_ascii=False, indent=4)


def run(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    main = BeautifulSoup(xml_data, 'xml')

    try:
        with_text_object, without_text_object = extract_data(main)
        splitting_path = file_path.replace('\\', '/')
        path_split = splitting_path.split('/')

        path_split[len(path_split) - 1] = path_split[-1].split('.xml')[0] + '.json'
        save_annotations(without_text_object, path_split, 'public_annotation')
        save_annotations(with_text_object, path_split, 'experiment_annotation')
    except ValueError:
        with open('no_citation.txt', 'a') as error_output:
            error_output.write(file_path + '\n')

if __name__ == '__main__':
    root_directory = 'data/uk'
    xml_files = find_xml_files(root_directory)
    # xml_files=['data/uk/uksc/2017/2.xml'] #testing purpose
    print(f'found {len(xml_files)} xml files')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_task = {executor.submit(run, task): task for task in xml_files}

        # Wrap the as_completed iterator with tqdm for a progress bar
        for future in tqdm(as_completed(future_to_task), total=len(future_to_task)):
            result = future.result()  # Get the result of the completed task
