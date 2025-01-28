# Multi-Omics Approaches for Understanding Gene-Environment Interactions in Noncommunicable Diseases: Techniques, Translation, and Equity Issues
# Authors: Robel Alemu, Nigussie T. Sharew, Yodit Y. Arsano, Muktar Ahmed, Fasil Tekola-Ayele, Tesfaye B. Mersha, Azmeraw T. Amare
# 
# This R script generates Figure 3: A Sankey diagram illustrating notable examples of gene-environment (GxE) interactions in non-communicable diseases (NCDs).
# The diagram is based on genome-wide GxE interaction and Mendelian randomization studies and visualizes how genetic and environmental factors influence NCD risk.
# Users should replace the file path to the input data with their own directory paths.
# 
# Dependencies: The script requires the `networkD3` and `htmlwidgets` R libraries.
# Install these packages if not already installed:
# install.packages("networkD3")
# install.packages("htmlwidgets")

# Load required libraries
library(networkD3)
library(htmlwidgets)

# Step 1: Read the input data
# Replace the file path with your own directory containing the input file
input_file <- "path/to/your/GxE_2.txt"  # Update with your file path
GxE_final <- read.delim(input_file)

# Step 2: Extract unique genes, environments, and phenotypes
genes <- unique(GxE_final$Genes)
environments <- unique(GxE_final$Environmental_exposure)
phenotypes <- unique(GxE_final$Phenotype)

# Step 3: Combine genes, environments, and phenotypes into a single list of nodes
nodes <- unique(c(genes, environments, phenotypes))

# Step 4: Create a data frame for the nodes
# Add metadata for node type and coloring
nodes_df <- data.frame(
  name = nodes,
  type = c(
    rep("gene", length(genes)), 
    rep("environment", length(environments)), 
    rep("phenotype", length(phenotypes))
  ),
  NodeGroup = "type_c"  # Uniform coloring for nodes
)

# Step 5: Create a data frame for the links
# Links from genes to environmental exposures
links_df <- data.frame(
  source = match(GxE_final$Genes, nodes) - 1,  # Node index for genes
  target = match(GxE_final$Environmental_exposure, nodes) - 1,  # Node index for environments
  value = 1,  # Default value for all links
  interaction = GxE_final$interaction_type  # Positive or negative interaction
)

# Links from environments to phenotypes
phenotype_links <- data.frame(
  source = match(GxE_final$Environmental_exposure, nodes) - 1,  # Node index for environments
  target = match(GxE_final$Phenotype, nodes) - 1,  # Node index for phenotypes
  value = 1,  # Default value for all links
  interaction = GxE_final$interaction_type  # Positive or negative interaction
)

# Combine all links into a single data frame
links_df <- rbind(links_df, phenotype_links)

# Step 6: Define link colors based on interaction type
links_df$LinkGroup <- ifelse(links_df$interaction == "positive", "type_a", "type_b")

# Step 7: Define the color scale for nodes and links
ColourScal <- 'd3.scaleOrdinal()
               .domain(["type_c", "type_a", "type_b"])
               .range(["#000000", "#66c2a4", "#D8BFD8"])'

# Step 8: Create the Sankey diagram
sankey <- sankeyNetwork(
  Links = links_df,
  Nodes = nodes_df,
  Source = "source",
  Target = "target",
  Value = "value",
  NodeID = "name",
  NodeGroup = "NodeGroup",  # Node coloring
  LinkGroup = "LinkGroup",  # Link coloring
  sinksRight = FALSE,  # Nodes align left-to-right
  colourScale = JS(ColourScal),  # Apply custom color scale
  nodeWidth = 3, 
  fontSize = 18, 
  fontFamily = "Times New Roman", 
  nodePadding = 20
)

# Step 9: Save the plot as an interactive HTML file
# Replace with your desired file path
output_file <- "path/to/your/SankeyDiagram_GxE.html"  # Update with your file path
saveWidget(sankey, file = output_file)

# Step 10: View the plot in your browser
print(sankey)

# Notes:
# - This script is designed for use with a tab-delimited input file containing columns:
#   Genes, Environmental_exposure, Phenotype, and interaction_type.
# - Replace file paths with your local directories for the input and output files.