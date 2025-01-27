Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases: Techniques, Translation, and Equity Issues

Overview

This repository contains the scripts and resources associated with the manuscript:

“Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases: Techniques, Translation, and Equity Issues”

Authors:
Robel Alemu; Nigussie T. Sharew; Yodit Y. Arsano;
Muktar Ahmed; Fasil Tekola-Ayele; Tesfaye B. Mersha; Azmeraw T. Amare

Published in Human Genomics.

This repository includes the Python scripts used to generate the visualizations featured in the manuscript.

PubmedCitations_SeqCost_Trend.py (Generates Figure 1): Log-Transformed Trends in PubMed Citation Frequencies and Sequencing Costs (2000–2024). Visualizes the growth in PubMed citations 
for key terms (multi-omics, personalized medicine, and GxE interactions) alongside the decline in sequencing costs.

gwas_sampleSize_WorldMap.py (Generates Figure 5): Global Distribution of Total GWAS Sample Sizes by Country. Illustrates disparities in genetic research participation globally, based on GWAS sample sizes by country.
	
Requirements

Python Libraries

The scripts require the following Python libraries. Install them using pip:

pip install pandas matplotlib geopandas requests beautifulsoup4 openpyxl numpy

Input Data
PubMed Citation Trends:
The script retrieves PubMed citation counts using web scraping. Ensure internet access is enabled.
Sequencing Cost Data:
Download the cost data from the NHGRI Genome Sequencing Program.
GWAS Sample Data:
The GWAS sample size data is based on Mills, M.C., and Rahal, C. (2020) Nature Genetics, DOI: 10.1038/s41588-020-0580-y.
	
If you use this repository, please cite the manuscript:

Alemu, R., Sharew, N.T., Arsano, Y.Y., Ahmed, M., Tekola-Ayele, F., Mersha, T.B., Amare, A.T.
Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases: Techniques, Translation, and Equity Issues.
Human Genomics.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

PubMed data was retrieved using web scraping via Python’s requests and BeautifulSoup libraries.
Sequencing cost data was sourced from the National Human Genome Research Institute’s Genome Sequencing Program.
GWAS sample size data was based on the GWAS Diversity Monitor published by Mills and Rahal (2020).