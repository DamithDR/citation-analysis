from bs4 import BeautifulSoup

from processor.custom_xml_parser import extract_data
from util.file_handle import find_xml_files


def pre_process(main):
    for table in main.find_all("table"):
        table.decompose()
    return main


def run():
    root_directory = 'data/uk/'
    xml_files = find_xml_files(root_directory)
    # xml_files=['data/uk/uksc/2024/9.xml']
    print(f'found {len(xml_files)} xml files')
    for file_path in xml_files:
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_data = file.read()
        main = BeautifulSoup(xml_data, 'xml')

        with_text_object, without_text_object = extract_data(main)

        print(without_text_object)


if __name__ == '__main__':
    run()
