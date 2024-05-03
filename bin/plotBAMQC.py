import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os.path

# ---- SCATTERPLOT

# 1. Coverage accorss reference
def plot_coverage_across_reference(csv_file_path):
    data = pd.read_csv(csv_file_path)

    # Creating figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Adding traces
    fig.add_trace(
        go.Scatter(x=data['Position (bp)'], y=data['Coverage'], name="coverage data"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=data['Position (bp)'], y=data['Std'], name="std data"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Coverage across reference"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Position (bp)")

    # Set y-axes titles
    fig.update_yaxes(title_text="Coverage", secondary_y=False)
    fig.update_yaxes(title_text="Std", secondary_y=True)

    fig.write_html('cov_ax_ref.html')
    fig.show()

# Call the function with the desired file path
plot_coverage_across_reference("./BAMQC_csv's/cov_ax_ref.csv")

# ---- HISTOGRAM


def bamqc_histogram(csv_file_path,x_header,y_header,title,y_title):
    data = pd.read_csv(csv_file_path)
    fig = px.histogram(data, x=x_header, y=y_header,title=title)
    fig.update_layout(yaxis_title=y_title)

    file_name = os.path.basename(csv_file_path)
    rm_sf = file_name.removesuffix(".csv")
    name = "./html/{}.html".format(rm_sf)
    fig.write_html(name)
    fig.show()


# 2. Coverage Histogram
bamqc_histogram("./BAMQC_csv's/cov_hist.csv",
                        x_header = 'Coverage',
                        y_header = 'Number of genomic locations',
                        title = "Coverage Histogram",
                        y_title = "Sum of number of genomic locations")

# 3. Duplication Rate Histogram

bamqc_histogram("./BAMQC_csv's/dup_rate_hist.csv",
                'Duplication rate',
                'Coverage',
                'Duplication rate histogram',
                'Number of loci')


# 4. Mapping Quality Histogram
bamqc_histogram("./BAMQC_csv's/mappingQuality_hist.csv",
                'Mapping quality',
                'mapping quality',
                'Mapping quality histogram',
                'Number of genomic locations')

# ---- BAR GRAPH

def bamqc_bar_graph(csv,x_head,y_head,gr_title,yax_title):
    data = pd.read_csv(csv)

    fig = px.bar(data, x=x_head, y=y_head, title=gr_title)

    if yax_title:
        fig.update_layout(yaxis_title=yax_title)

    file_name = os.path.basename(csv)
    rm_sf = file_name.removesuffix(".csv")
    name = "./html/{}.html".format(rm_sf)
    fig.write_html(name)
    fig.show()

# 5. Genome Fraction Coverage

bamqc_bar_graph("./BAMQC_csv's/genome_frac_cov.csv",
                'Coverage (X)',
                'Coverage',
                'Genome fraction coverage',
                'Fraction of reference (%)')

# 6. Insert Size Histogram
bamqc_bar_graph("./BAMQC_csv's/insertSize_hist.csv",
                'Insert size (bp)',
                'insert size',
                'Insert size bar chart',
                'Number of reads')

# 7. Homopolymer Indel
data5 = pd.read_csv("./BAMQC_csv's/homopoly_indels.csv")
fig5 = px.bar(data5, x='Type of indel', y='Number of indels', color='Type of indel', title='Homopolymer indels')
fig5.write_html('homopoly_indels.html')
fig5.show()



# ---- LINE GRAPH

def bamqc_line_graph(file_path, x_column, y_columns, title, yaxis_title):

    data = pd.read_csv(file_path)
    fig = px.line(data, x=x_column, y=y_columns, title=title)

    if yaxis_title:
        fig.update_layout(yaxis_title=yaxis_title)

    file_name = os.path.basename(file_path)
    rm_sf = file_name.removesuffix(".csv")
    name = "./html/{}.html".format(rm_sf)
    fig.write_html(name)
    fig.show()

# 8. Insert Size Across Reference
bamqc_line_graph("./BAMQC_csv's/insertSize_ax_ref.csv",
                'Position (bp)',
                'insert size',
                'Insert size across reference',
                None)

# 9. Mapped Reads Clipping Profile
bamqc_line_graph("./BAMQC_csv's/mappedReads_clip_profile.csv",
                'Read position (bp)',
                'Clipping profile',
                'Mapped reads clipping profile',
                'Clipped bases (%)')

# 10. Mapped Reads GC Content Distribution
bamqc_line_graph("./BAMQC_csv's/mappedReads_gc_content_dist.csv",
                'GC Content (%)',
                'Sample',
                'Mapped reads GC-content distribution',
                'Fraction of reads')

# 11. Mapped Reads GC Nucleotide Content
bamqc_line_graph("./BAMQC_csv's/mappedReads_gc_nucleotide_content.csv",
                ' Position (bp)',
                ['A', 'C', 'G', 'T', 'N'],
                'Mapped reads nucleotide content',
                'Nucleotides Content (%)')

# 12. Mapping Quality Across Reference
bamqc_line_graph("./BAMQC_csv's/mappingQuality_ax_ref.csv",
                'Position (bp)',
                'mapping quality',
                'Mapping quality across reference',
                None)