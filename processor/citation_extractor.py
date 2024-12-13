import re


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
