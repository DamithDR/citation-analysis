import json
import matplotlib.pyplot as plt
from tqdm import tqdm

dataset = 'dataset/public_annotation_backup.json'

with open(dataset, 'r', encoding="utf-8") as f:
    dataset = json.loads(f.read())

case_wise_total_citation_counts = []
no_citation_cases = 0
cases_with_any_citation = 0
print(f'Total number of cases {len(dataset)}')
for data in tqdm(dataset):
    found = False
    keys = data['sequence']
    total_citations = 0
    for key in keys:
        case_paragraph = data['paragraphs'][key]
        if len(case_paragraph['neutral_citations']) > 0:
            found = True

            for citation in case_paragraph['neutral_citations']:
                total_citations += len(citation['paragraphs'])
    if not found:
        no_citation_cases += 1
    else:
        cases_with_any_citation += 1
    case_wise_total_citation_counts.append(total_citations)

# Create the histogram
case_wise_total_citation_counts = [x for x in case_wise_total_citation_counts if x != 0]
bins = [i for i in range(0, 45)]
counts, bins, patches = plt.hist(case_wise_total_citation_counts, bins=bins, edgecolor='black', alpha=0.7)

print(f'cases without any citations {no_citation_cases}')
print(f'cases without some citations {cases_with_any_citation}')
print(f'cases with paragraph citations {len(case_wise_total_citation_counts)}')

print(f'total count = {len(dataset)}')

# Add labels and title
plt.title("Histogram of Data with Frequencies")
plt.xlabel("Value")
plt.ylabel("Frequency")

# Annotate each bar with its frequency
for count, bin_start, patch in zip(counts, bins, patches):
    bin_center = bin_start + (bins[1] - bins[0]) / 2  # Calculate bin center
    plt.text(bin_center, count, str(int(count)), ha='center', va='bottom', fontsize=8)

# Show the plot
plt.show()
