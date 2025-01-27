"""
Title: Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases: Techniques, Translation, and Equity Issues

Authors: Robel Alemu, Nigussie T. Sharew, Yodit Y. Arsano, 
         Muktar Ahmed, Fasil Tekola-Ayele, Tesfaye B. Mersha, Azmeraw T. Amare
         
Figure 1. Log-Transformed Trends in PubMed Citation Frequencies and Sequencing Costs (2000–2024)

Description:
This script generates a dual-axis plot illustrating trends in sequencing costs and PubMed citation frequencies 
for key terms ("multi-omics," "personalized/precision medicine," and "gene-environment (GxE) interactions") 
from 2000 to 2024. Citation data were retrieved via a Python-based web scraping approach, while sequencing 
cost data were sourced from the National Human Genome Research Institute (NHGRI). Both axes represent 
log10-transformed values to visualize exponential trends effectively.
"""

# Step 1: Import required libraries
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from matplotlib.ticker import FuncFormatter
import numpy as np

# Step 2: Define the range of years for the analysis
years = range(2000, 2024)  # Includes 2024 for future projections

# Step 3: Initialize dictionaries to store citation data by category
citations_per_year_multiomics = {}
citations_per_year_personalized_medicine = {}
citations_per_year_gxe = {}

# Step 4: Set the base URL for PubMed searches
base_url = "https://pubmed.ncbi.nlm.nih.gov"

# Step 5: Function to fetch citation counts from PubMed
def get_citations(year, query_terms):
    """
    Fetches the number of citations from PubMed for a specific year and query terms.

    Args:
    - year (int): The year for which citation data is retrieved.
    - query_terms (list of str): List of keywords to search in PubMed.

    Returns:
    - int: Citation count for the given year and query terms.
    """
    query = f"({' OR '.join(query_terms)})[Title/Abstract] AND {year}[Date - Publication]"
    url = f"{base_url}/?term={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results_div = soup.find('div', {'class': 'results-amount'})
    if results_div and results_div.span:
        results_info = results_div.span.get_text()
        return int(results_info.split()[0].replace(',', ''))
    else:
        return 0

# Step 6: Define search terms for the three categories
multiomics_terms = ["multiomics", "multi-omics", "Multiomics", "Multi-omics"]
personalized_medicine_terms = ["personalized-medicine", "precision-medicine", "personalized medicine", "precision medicine"]
gxe_terms = ["gene-environment interaction", "gene-environment correlation", "GxE interaction", "GxE"]

# Step 7: Loop through each year and retrieve citation counts for each category
for year in years:
    citations_per_year_multiomics[year] = get_citations(year, multiomics_terms)
    citations_per_year_personalized_medicine[year] = get_citations(year, personalized_medicine_terms)
    citations_per_year_gxe[year] = get_citations(year, gxe_terms)

# Step 8: Load and preprocess sequencing cost data
cost_data = pd.read_excel('/disk/XX/misc/adelaide/Sequencing_Cost_Data_Table_May2022.xls', usecols=["Date", "Cost per Mb"])
cost_data['Year'] = pd.to_datetime(cost_data['Date'], errors='coerce').dt.year
cost_data_grouped = cost_data.groupby('Year')['Cost per Mb'].mean().reset_index()

# Step 9: Prepare log-transformed citation data for plotting
log_citations_multiomics = {k: np.log10(v) if v > 0 else 0 for k, v in citations_per_year_multiomics.items()}
log_citations_personalized_medicine = {k: np.log10(v) if v > 0 else 0 for k, v in citations_per_year_personalized_medicine.items()}
log_citations_gxe = {k: np.log10(v) if v > 0 else 0 for k, v in citations_per_year_gxe.items()}

# Step 10: Log-transform sequencing cost data
cost_data_grouped['Log_Cost_per_Mb'] = np.log10(cost_data_grouped['Cost per Mb'])

# Step 11: Plotting the data
fig, ax1 = plt.subplots(figsize=(14, 10))

# Plot citation data
ax1.plot(log_citations_multiomics.keys(), log_citations_multiomics.values(), color='blue', label='Multi-Omics (Log Transformed)', marker='o')
ax1.plot(log_citations_personalized_medicine.keys(), log_citations_personalized_medicine.values(), color='red', label='Personalized Medicine (Log Transformed)', marker='o')
ax1.plot(log_citations_gxe.keys(), log_citations_gxe.values(), color='black', label='GxE Interaction (Log Transformed)', marker='x')

# Configure y-axis for citation data
ax1.set_ylabel('Log10(Number of Citations)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Format y-axis for citation data
citation_min = np.floor(min(log_citations_multiomics.values()) * 2) / 2
citation_max = np.ceil(max(log_citations_multiomics.values()) * 2) / 2
ax1.set_yticks(np.arange(citation_min, citation_max + 0.5, 0.5))
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}'))

# Add sequencing cost data to a secondary axis
ax2 = ax1.twinx()
ax2.plot(cost_data_grouped['Year'], cost_data_grouped['Log_Cost_per_Mb'], color='green', label='Cost per Mb (Log Transformed)', marker='s')

# Configure y-axis for sequencing cost data
ax2.set_ylabel('Log10(Cost per Mb in $)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Format y-axis for sequencing cost data
cost_min = np.floor(cost_data_grouped['Log_Cost_per_Mb'].min() * 2) / 2
cost_max = np.ceil(cost_data_grouped['Log_Cost_per_Mb'].max() * 2) / 2
ax2.set_yticks(np.arange(cost_min, cost_max + 0.5, 0.5))
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}'))

# Add title, grid, and legends
ax1.set_title('Log-Transformed Trends in PubMed Citations and Sequencing Cost (2000–2024)')
ax1.grid(True, linestyle='--', linewidth=0.5)
ax1.set_xticks(range(min(years), max(years) + 1, 3))  # Set x-tick interval

# Position legends
ax1.legend(loc='upper left', bbox_to_anchor=(0.0, -0.07))  # Citation legend
ax2.legend(loc='upper right', bbox_to_anchor=(1.0, -0.07))  # Cost legend

# Save the figure
save_path = '/disk/XX/misc/adelaide/multiomics_personalized_medicine_cost_per_mb_trend_refined.png'
plt.savefig(save_path, bbox_inches='tight')
plt.show()
