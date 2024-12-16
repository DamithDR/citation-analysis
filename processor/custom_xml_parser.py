import re


def extract_data(main):
    citation = get_citation(main)
    date = get_date(main)
    url = get_url(main)
    paragraphs, no_text_paragraphs, full_text = get_paragraphs_with_citations(main)
    with_text_object = {'neutral_citation': citation, 'judgment_date': date, 'url': url, 'paragraphs': paragraphs,
                        'full_text': full_text}
    without_text_object = {'neutral_citation': citation, 'judgment_date': date, 'url': url,
                           'paragraphs': no_text_paragraphs}
    return with_text_object, without_text_object


def get_citation(main):
    citation = main.find('neutralCitation')
    if citation is None:
        citation = main.find('header').find('neutralCitation')
        if citation is not None:
            citation = citation.text.strip()
        else:
            prop = main.find('meta').find('proprietary')
            if prop is not None:
                citation = extract_neutral_citations(prop.text)
    else:
        citation = citation.text.strip()
    return citation


def get_date(main):
    date = main.find('FRBRExpression').find('FRBRdate')['date'].strip()
    return date


def get_url(main):
    return main.find('FRBRExpression').find('FRBRuri')['value'].strip()


def extract_other_citations(para):
    pattern = r'\(\d{4}\) \d{1,2} [A-Z]+ \d+'  # simple but need to improve
    citations = re.findall(pattern, para)
    return citations


def remove_citations_from_text(para, citation_types):
    for citation_type in citation_types:
        for citation in citation_type:
            para = para.replace(citation, 'CITATION')  # remove citation from original text
    return para


def get_paragraphs_with_citations(main):
    body = main.find('judgmentBody')
    paragraphs = body.find_all('paragraph', eId=True)
    paragraphs_dict = {}
    no_text_paragraphs_dict = {}
    full_text = ''
    for para in paragraphs:

        para_number = para.findNext('num')
        if para_number is not None:
            para_number = para_number.text.strip()
            para = clean_paragraph_text(para.text.strip())
            neutral_citations = extract_neutral_citations(para)
            other_citations = extract_other_citations(para)

            para = remove_citations_from_text(para, [neutral_citations, other_citations])
            paragraphs_dict[para_number] = {'paragraph': para, 'neutral_citations': neutral_citations,
                                            'other_citations': other_citations}
            no_text_paragraphs_dict[para_number] = {'neutral_citations': neutral_citations,
                                                    'other_citations': other_citations}
            full_text += "\n" + para
        else:
            continue
    return paragraphs_dict, no_text_paragraphs_dict, full_text


def clean_paragraph_text(text):
    # Remove multiple spaces and replace them with a single space
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_neutral_citations(document):
    """
    Extracts all neutral citations from a given document based on predefined patterns.

    Args:
        document (str): The text document containing potential neutral citations.

    Returns:
        list: A list of extracted citations in their full citation format.
    """
    # Define the regex pattern
    pattern = r"""
        (\[\d{4}\])                  # Match the year in square brackets
        \s+([A-Za-z]+)                # Match any word or abbreviation for the court identifier
        \s+(D?\d+)                    # Match 'D' optionally followed by the case number
        (?:                             # Start of optional group for sub-divisions
            \s*\((Admin|Ch|Pat|QB|KB|Comm|Admlty|TCC|Fam|Mercantile|SCCO|IPEC|AAC|IAC|LC|TC|GRC)?\)
        )?                              # End of optional group
    """

    # Compile the pattern with verbose mode for readability
    regex = re.compile(pattern, re.VERBOSE)

    # Find all matches
    matches = regex.findall(document)

    # Format the matches into full citation format
    citations = []
    for match in matches:
        citation = match[0] + " " + match[1] + " " + match[2]
        if match[3]:
            citation += " (" + match[3] + ")"
        citations.append(citation)

    return citations
