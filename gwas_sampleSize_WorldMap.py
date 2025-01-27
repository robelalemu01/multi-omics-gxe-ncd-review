"""
Title: Global Distribution of Total GWAS Sample Sizes by Country
Authors: Robel Alemu, Nigussie T. Sharew, Yodit Y. Arsano, 
         Muktar Ahmed, Fasil Tekola-Ayele, Tesfaye B. Mersha, Azmeraw T. Amare

Figure 5. Global Distribution of Total GWAS Sample Sizes by Country. 

Description:
This script generates a global map showing the cumulative GWAS sample sizes across various countries,
highlighting global disparities in genetic research participation. The data and methodology align with the manuscript:
"Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases:
Techniques, Translation, and Equity Issues."

Data Source:
Mills, M.C., and Rahal, C. (2020). "The GWAS Diversity Monitor Tracks Diversity by Disease in real-time."
Nature Genetics, 52, pp. 242-243. DOI: 10.1038/s41588-020-0580-y.

Steps:
1. Import necessary libraries.
2. Load and process GWAS data.
3. Categorize sample sizes into meaningful groups.
4. Merge sample size data with world shape files.
5. Plot the global map with customized visualization.
6. Save the output figure for inclusion in the manuscript.

"""

# Step 1: Import necessary libraries
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Step 2: Load the GWAS data
data = pd.read_csv('/disk/XX/GWASmonitor_Data.csv')

# Correct country names for consistency
data['index'] = data['index'].replace('Korea, South', 'South Korea')

# Aggregate sample sizes across years for each country
aggregated_data = data.groupby('index').agg({'N': 'sum'}).reset_index()

# Step 3: Categorize sample sizes into meaningful groups
categories = {
    '>1 million': '#042037',    # Very dark blue
    '100k-1M': '#084594',       # Medium blue
    '5k-100k': '#6baed6',       # Lighter blue
    '501-5k': '#bfd3e6',        # Very light blue
    '101-500': '#d9e2f8',       # Near white blue
    '1-100': '#f0f5fc',         # Almost white
    '0': '#ffffff',             # White
    'No Data': '#ffffff'        # White for no data
}

# Function to assign categories based on sample size
def categorize_sample_size(n):
    if n > 1000000:
        return '>1 million'
    elif n > 100000:
        return '100k-1M'
    elif n > 5000:
        return '5k-100k'
    elif n > 500:
        return '501-5k'
    elif n > 100:
        return '101-500'
    elif n > 0:
        return '1-100'
    else:
        return '0'

# Apply categorization to the data
aggregated_data['sample_size_category'] = aggregated_data['N'].apply(categorize_sample_size)
aggregated_data['sample_size_category'] = pd.Categorical(aggregated_data['sample_size_category'], 
                                                         categories=categories.keys(), 
                                                         ordered=True)
# Adjust United States name to match GeoDataFrame
aggregated_data.loc[aggregated_data['index'] == 'United States', 'index'] = 'United States of America'

# Step 4: Merge the GWAS data with world shape files
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[world['continent'] != 'Antarctica']  # Exclude Antarctica
world = world.merge(aggregated_data, how='left', left_on='name', right_on='index')

# Set "No Data" explicitly for countries not in the dataset
world['sample_size_category'] = world['sample_size_category'].fillna('No Data')

# Step 5: Create the map visualization
fig, ax = plt.subplots(1, 1, figsize=(25, 15))

# Plot country boundaries
world.boundary.plot(ax=ax, color='black', linewidth=0.5)

# Plot countries with categorized sample sizes
category_colors = ListedColormap([categories[cat] for cat in categories.keys()])
world.plot(column='sample_size_category', ax=ax, legend=False, cmap=category_colors)

# Create a custom legend
legend_labels = {key: Patch(facecolor=color, edgecolor=color) for key, color in categories.items()}
ax.legend(handles=[legend_labels[key] for key in legend_labels],
          labels=[key for key in legend_labels],
          title='GWAS Sample Size',
          loc='lower left',
          bbox_to_anchor=(-0.05, -0.05),  # Adjust legend position
          fontsize=16,
          title_fontsize=20)

# Title and formatting
plt.title('Global Distribution of Total GWAS Sample Sizes by Country', fontsize=20, pad=20)
ax.axis('off')  # Remove axis lines and ticks

# Step 6: Save the figure
plt.savefig('/disk/CC/GWAS_population_adjusted_map.png', bbox_inches='tight')
plt.show()
