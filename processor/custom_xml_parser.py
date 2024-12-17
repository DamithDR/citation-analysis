import re


def extract_data(main):
    citation = get_citation(main)
    if citation is None:
        raise ValueError('citation not found')
    elif isinstance(citation, list):
        citation = citation[0]
    date = get_date(main)
    url = get_url(main)
    paragraphs, no_text_paragraphs, full_text, key_sequence = get_paragraphs_with_citations(main)
    with_text_object = {'neutral_citation': citation, 'judgment_date': date, 'url': url, 'paragraphs': paragraphs,
                        'full_text': full_text, 'sequence': key_sequence}
    without_text_object = {'neutral_citation': citation, 'judgment_date': date, 'url': url,
                           'paragraphs': no_text_paragraphs, 'sequence': key_sequence}
    return with_text_object, without_text_object


def get_citation(main):
    citation = main.find('neutralCitation')
    if citation is None:
        if main.find('header') is not None:
            citation = main.find('header').find('neutralCitation')

        if citation is not None:
            citation = citation.text.strip()
        else:
            meta = main.find('meta')
            if meta is not None:
                prop = meta.find('proprietary')
                if prop is not None:
                    citation = extract_neutral_citations(prop.text)
                else:
                    citation = None
            else:
                citation = None
    else:
        citation = citation.text.strip()
    return citation


def get_date(main):
    date = main.find('FRBRExpression').find('FRBRdate')['date'].strip()
    return date


def get_url(main):
    return main.find('FRBRExpression').find('FRBRuri')['value'].strip()


def extract_other_citations(para):
    citations = []
    pattern = r"\[\d{4}\] \d+ [A-Z]{2,5} \d+"
    citations.extend(re.findall(pattern, para))
    pattern2 = r"\[\d{4}\] [A-Z]{2,5} \d+"
    citations.extend(re.findall(pattern2, para))

    return citations


def remove_citations_from_text(para, citation_types):
    for citation_type in citation_types:
        for citation in citation_type:
            para = para.replace(citation, 'CITATION')  # remove citation from original text
    return para


def get_paragraphs_with_citations(main):
    body = main.find('judgmentBody')
    paragraphs = body.find_all('paragraph', eId=True)
    if len(paragraphs) == 0:
        paragraphs = body.find_all('paragraph')
    paragraphs_dict = {}
    no_text_paragraphs_dict = {}
    full_text = []
    key_sequence = []
    for para in paragraphs:

        para_number = para.findNext('num')
        if para_number is not None:
            para_number = para_number.text.strip()
            para = clean_paragraph_text(para.text.strip())
            neutral_citations = extract_neutral_citations(para)
            para = remove_citations_from_text(para, [neutral_citations])
            other_citations = extract_other_citations(para)
            para = remove_citations_from_text(para,
                                              [other_citations])  # progressively remove citations to avoid duplicates

            if para_number in paragraphs_dict.keys():
                para_number = f'{para_number}_{para_number}'
            paragraphs_dict[para_number] = {'paragraph': para, 'neutral_citations': neutral_citations,
                                            'other_citations': other_citations}
            no_text_paragraphs_dict[para_number] = {'neutral_citations': neutral_citations,
                                                    'other_citations': other_citations}
            full_text.append(para)
            key_sequence.append(para_number)
        else:
            continue
    return paragraphs_dict, no_text_paragraphs_dict, full_text, key_sequence


def clean_paragraph_text(text):
    # Remove multiple spaces and replace them with a single space
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_neutral_citations(document):
    # Regular expressions for each court type
    regex_ukpc = re.compile(r"\[\d{4}\]\sUKPC(?:\s[A-Za-z]+)?\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewca = re.compile(r"\[\d{4}\]\sEWCA(?:\s[A-Za-z]+)?\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewhc = re.compile(r"\[\d{4}\]\sEWHC(?:\s[A-Za-z]+)?\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_uksc = re.compile(r"\[\d{4}\]\sUKSC\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewfc = re.compile(r"\[\d{4}\]\sEWFC\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewcop = re.compile(r"\[\d{4}\]\sEWCOP\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_cat = re.compile(r"\[\d{4}\]\sCAT\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ukut = re.compile(r"\[\d{4}\]\sUKUT\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ukiptrib = re.compile(r"\[\d{4}\]\sUKIPTrib\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_eat = re.compile(r"\[\d{4}\]\sEAT\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ukftt = re.compile(r"\[\d{4}\]\sUKFTT\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewcr = re.compile(r"\[\d{4}\]\sEWCR\s\d+(?:\s?\([A-Za-z]+\))?")
    regex_ewcc = re.compile(r"\[\d{4}\]\sEWCC\s\d+(?:\s?\([A-Za-z]+\))?")

    # Extracting matches for each court type
    matches_ukpc = regex_ukpc.findall(document)
    matches_ewca = regex_ewca.findall(document)
    matches_ewhc = regex_ewhc.findall(document)
    matches_uksc = regex_uksc.findall(document)
    matches_ewfc = regex_ewfc.findall(document)
    matches_ewcop = regex_ewcop.findall(document)
    matches_cat = regex_cat.findall(document)
    matches_ukut = regex_ukut.findall(document)
    matches_ukiptrib = regex_ukiptrib.findall(document)
    matches_eat = regex_eat.findall(document)
    matches_ukftt = regex_ukftt.findall(document)
    matches_ewcr = regex_ewcr.findall(document)
    matches_ewcc = regex_ewcc.findall(document)

    all_matches = [
        match for match_list in [
            matches_ukpc, matches_ewca, matches_ewhc, matches_uksc, matches_ewfc,
            matches_ewcop, matches_cat, matches_ukut, matches_ukiptrib, matches_eat,
            matches_ukftt, matches_ewcr, matches_ewcc
        ] for match in match_list if match
    ]

    return all_matches
