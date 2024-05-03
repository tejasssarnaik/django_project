
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



# ### Coverage Across Reference


data = pd.read_csv("./BAMQC_csv's/cov_ax_ref.csv")
data


# Creating figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Adding traces
fig.add_trace(
    go.Scatter(x=data['Position (bp)'], y=data['Coverage'], name="coverage data"),
    secondary_y = False,
)

fig.add_trace(
    go.Scatter(x=data['Position (bp)'], y=data['Std'], name="std data"),
    secondary_y = True,
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
# fig.show()


# ### Coverage Histogram


data2 = pd.read_csv("./BAMQC_csv's/cov_hist.csv")
data2


fig2 = px.histogram(data2, x='Coverage', y='Number of genomic locations')

fig2.update_layout(
    title_text="Coverage Histogram",
    yaxis_title="Sum of number of genomics locations"
)

fig2.show()


# ### Duplication Rate Histogram


data3 = pd.read_csv("./BAMQC_csv's/dup_rate_hist.csv")
data3


fig3 = px.histogram(data3, x='Duplication rate', y='Coverage', title='Duplication rate histogram')
fig3.update_layout(
    yaxis_title = 'Number of loci'
)
fig3.show()


# ### Genome Fraction Coverage


data4 = pd.read_csv("./BAMQC_csv's/genome_frac_cov.csv")
data4


fig4 = px.bar(data4, x='Coverage (X)', y='Coverage', title='Genome fraction coverage')
fig4.update_layout(
    yaxis_title = 'Fraction of reference (%)'
)
fig4.write_html('genome_frac_cov.html')
# fig4.show()


# ### Homopolymer Indel


data5 = pd.read_csv("./BAMQC_csv's/homopoly_indels.csv")
data5


fig5 = px.bar(data5, x='Type of indel', y='Number of indels', color='Type of indel', title='Homopolymer indels')
fig5.write_html('homopoly_indels.html')
# fig5.show()


# ### Insert Size Across Reference


data6 = pd.read_csv("./BAMQC_csv's/insertSize_ax_ref.csv")
data6


fig6 = px.line(data6, x='Position (bp)', y='insert size', title='Insert size across reference')
fig6.write_html('insertSize_ax_ref.html')
# fig6.show()


# ### Insert Size Histogram


data7 = pd.read_csv("./BAMQC_csv's/insertSize_hist.csv")
data7


fig7 = px.bar(data7, x='Insert size (bp)', y='insert size', title='Insert size bar chart')
fig7.update_layout(
    yaxis_title = 'Number of reads'
)
fig7.write_html('insertSize_hist.html')
# fig7.show()


# ### Mapped Reads Clipping Profile


data8 = pd.read_csv("./BAMQC_csv's/mappedReads_clip_profile.csv")
data8



fig8 = px.line(data8, x='Read position (bp)', y='Clipping profile', title='Mapped reads clipping profile')
fig8.update_layout(
    yaxis_title = 'Clipped bases (%)'
)
fig8.show()


# ### Mapped Reads GC Content Distribution


data9 = pd.read_csv("./BAMQC_csv's/mappedReads_gc_content_dist.csv")
data9


fig9 = px.line(data9, x='GC Content (%)', y='Sample', title='Mapped reads GC-content distribution')
fig9.update_layout(
    yaxis_title='Fraction of reads'   
)
fig9.write_html('mappedReads_gc_content_dist.html')
# fig9.show()


# ## Mapped Reads GC Nucleotide Content


data10 = pd.read_csv("./BAMQC_csv's/mappedReads_gc_nucleotide_content.csv")
data10


fig10 = px.line(data10, x=' Position (bp)', y=['A', 'C', 'G', 'T', 'N'], title='Mapped reads nucleotide content')
fig10.update_layout(
    yaxis_title = 'Nucleotides Content (%)'
)
fig10.show()


# ### Mapping Quality Across Reference


data11 = pd.read_csv("./BAMQC_csv's/mappingQuality_ax_ref.csv")
data11


fig11 = px.line(data11, x='Position (bp)', y='mapping quality', title='Mapping quality across reference')
fig11.write_html('mappingQuality_ax_ref.html')
# fig11.show()


# ### Mapping Quality Histogram


data12 = pd.read_csv("./BAMQC_csv's\mappingQuality_hist.csv")

data12


fig12 = px.histogram(data12, x='Mapping quality', y='mapping quality', title='Mapping quality histogram')
fig12.update_layout(
    yaxis_title = 'Number of genomic locations'
)
fig12.show()





