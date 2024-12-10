import re

from bs4 import BeautifulSoup


def clean_paragraph_text(text):
    # Remove multiple spaces and replace them with a single space
    text = re.sub(r'\s+', ' ', text)
    return text


def run():

    with open('data/uk/uksc/2011/39.xml', 'r') as file:
        xml_data = file.read()
    main = BeautifulSoup(xml_data, 'xml')

    print(main.find('neutralCitation').text.strip())
    print(main.find('FRBRname')['value'].strip())
    print(main.find('FRBRExpression').find('FRBRdate')['date'].strip())
    print(main.find('FRBRExpression').find('FRBRuri')['value'].strip())

    soup = main.find('header')
    # Extracting elements
    term = soup.find('span', style=lambda s: s and "font-weight:bold" in s).text.strip()
    neutral_citation = soup.find('neutralCitation').text.strip()
    appeal_from = soup.find('ref')['uk:canonical']
    judgment_title = soup.find('span', style=lambda s: s and "font-weight:bold;font-size:20pt" in s).text.strip()
    parties = {
        "appellant": soup.find('party', attrs={'as': '#appellant'}).text.strip(),
        "respondent": soup.find('party',attrs={'as': "#respondent"} ).text.strip()
    }
    roles = {
        "appellant_role": soup.find('role', refersTo="#appellant").text.strip(),
        "respondent_role": soup.find('role', refersTo="#respondent").text.strip()
    }
    judges = [judge.text.strip() for judge in soup.find_all('span', style=lambda s: s and "font-weight:bold;font-size:17pt" in s)]
    judgment_date = soup.find('docDate')['date']
    heard_on = soup.find('span', style=lambda s: s and "font-weight:bold;font-size:15pt" in s).text.strip()

    # Counsels for both parties
    counsels = {
        "appellants_counsel": [p.text.strip() for p in soup.select('table:nth-of-type(2) tr td:nth-of-type(1) p span')],
        "respondents_counsel": [p.text.strip() for p in soup.select('table:nth-of-type(2) tr td:nth-of-type(3) p span')]
    }

    # Output extracted information
    print("Term:", term)
    print("Neutral Citation:", neutral_citation)
    print("Appeal From:", appeal_from)
    print("Judgment Title:", judgment_title)
    print("Parties:", parties)
    print("Roles:", roles)
    print("Judges:", judges)
    print("Judgment Date:", judgment_date)
    print("Heard On:", heard_on)
    print("Counsels:", counsels)

    body = main.find('judgmentBody')
    paragraphs = body.find_all('paragraph', eId=True)
    # paragraphs = extract_paragraphs(text)

    for para in paragraphs:
        print(para.findNext('num').text.strip())
        print(clean_paragraph_text(para.text.strip()))
        print('===========================================================')


if __name__ == '__main__':
    run()