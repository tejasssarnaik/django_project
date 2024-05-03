import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("SRR21615284_gavcf1_actionable_variants.txt", sep="\t")
data


#to covert the value counts result in to a data frame
clnsig_data = data["CLNSIG"].value_counts().rename_axis('clnsig').reset_index(name='counts')
#to drop rows containing following values
# clnsig_data.drop(['Benign', 'Benign/Likely_benign', 'Likely_benign'], inplace=True)

clnsig_data


clnsig_data.to_csv('clnsig_data', index=False)
df = pd.read_csv("clnsig_data", index_col='clnsig')
df

 [markdown]
# PATHOGENIC


#Pathogenic
d = {'clnsig':[], 'counts':[]}
items = df.loc[['Pathogenic', 'Pathogenic|risk_factor', 'Likely_pathogenic']]
sum = int(items.sum())
inc_count = sum*10

d['clnsig'].append('Pathogenic')
d['counts'].append(sum)

 [markdown]
# DRUG RESPONSE


#drug_response
items = df.loc[['drug_response', 'Conflicting_interpretations_of_pathogenicity|drug_response|other', 'Uncertain_significance|drug_response', 'association|drug_response', 'Benign|drug_response']]
sum2 = int(items.sum())
inc_count = sum2*10

d['clnsig'].append('Drug_response')
d['counts'].append(sum2)

 [markdown]
# AFFECTS


#Affects
items = df.loc[['Affects', 'Conflicting_interpretations_of_pathogenicity|Affects']]
sum3 = int(items.sum())
inc_count = sum3*10

d['clnsig'].append('Affects')
d['counts'].append(sum3)

 [markdown]
# ASSOCIATION


#association
items = df.loc[['association', 'association|drug_response']]
sum4 = int(items.sum())
inc_count = sum4*10

d['clnsig'].append('Association')
d['counts'].append(sum4)

 [markdown]
# PROTECTIVE


#protective
items = df.loc[['protective', 'Benign|protective', 'Uncertain_risk_allele|protective']]
sum5 = int(items.sum())
inc_count = sum5*10

d['clnsig'].append('Protective')
d['counts'].append(sum5)

 [markdown]
# RISK FACTOR


#risk_factor
items = df.loc[['risk_factor', 'Pathogenic|risk_factor', 'Uncertain_significance|risk_factor', 'Conflicting_interpretations_of_pathogenicity|risk_factor']]
sum6 = int(items.sum())
inc_count = sum6*10

d['clnsig'].append('Risk_factor')
d['counts'].append(sum6)

 [markdown]
# BENIGN


dict1 = {'clnsig':[], 'counts':[]}
items = df.loc[['Benign', 'Benign/Likely_benign', 'Likely_benign', 'Benign|other', 'Benign|drug_response', 'Benign|protective', 'Likely_benign|other']]
s = int(items.sum())

dict1['clnsig'].append('Benign')
dict1['counts'].append(s)

 [markdown]
# UNCERTAIN SIGNIFICANCE


#Uncertain_significance
items = df.loc[['Conflicting_interpretations_of_pathogenicity', 'Conflicting_interpretations_of_pathogenicity|drug_response|other', 'Conflicting_interpretations_of_pathogenicity|Affects', 'Conflicting_interpretations_of_pathogenicity|risk_factor', 'Uncertain_significance', 'Uncertain_significance|risk_factor', 'Uncertain_significance|drug_response']]
sum1 = int(items.sum())
inc_count = sum1*10

dict1['clnsig'].append('Uncertain_significance')
dict1['counts'].append(sum1)


del dict1
del d


DF = pd.DataFrame(d)
ddf = pd.DataFrame(dict1)
ddf
DF


# del dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots

label = np.array(DF['clnsig'])
y_coords = np.array(DF['counts'])

labels = np.array(ddf['clnsig'])
y_vals = np.array(ddf['counts'])

fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])

# fig.add_trace(px.pie(DF, names='clnsig', values='counts'), 1, 1)
fig.add_trace(go.Pie(labels=label, values=y_coords, hoverlabel=dict(font=dict(color='white'))), 1, 1)

# fig.add_trace(px.pie(df, names='Benign', values='Others'), 1, 2)
fig.add_trace(go.Pie(labels=labels, values=y_vals, hoverlabel=dict(font=dict(color='white'))), 1, 2)


fig.update_layout(height=400, width=1000, title_text='Clinical Significance')

dict = dict(
    orientation="h",
    entrywidth=100,
    font=dict(color='black')

)

# dictt = dict(size=9,color='black')
fig.update_layout(legend=dict)
fig.update_traces(hovertemplate="<b>%{label} </b><br>" +
                  "<b>%{value} </b><br>" +
                  "<extra></extra>")
# fig.update_traces(visible = 'legendonly')

# fig.update_layout(legend_tracegroupgap=30)



fig.write_html('pie.html')
# fig.show()

        





