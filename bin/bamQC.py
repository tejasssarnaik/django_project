
import pandas as pd
import plotly.express as px

# coverage_across_reference

mylines = ""
col_name = []
row_vals = []


with open ('./txt_files/coverage_across_reference.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("cov_ax_ref.csv", "w") as op:
        op.write(mylines)
        op.close()



# coverage_histogram

mylines = ""
col_name = []
row_vals = []


with open ('./txt_files/coverage_histogram.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("cov_hist.csv", "w") as op:
        op.write(mylines)
        op.close()



# duplication_rate_histogram


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/duplication_rate_histogram.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("dup_rate_hist.csv", "w") as op:
        op.write(mylines)
        op.close()


# genome_fraction_coverage
mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/genome_fraction_coverage.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("genome_frac_cov.csv", "w") as op:
        op.write(mylines)
        op.close()


# homopolymer_indels


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/homopolymer_indels.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("homopoly_indels.csv", "w") as op:
        op.write(mylines)
        op.close()


# insert_size_across_reference


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/insert_size_across_reference.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("insertSize_ax_ref.csv", "w") as op:
        op.write(mylines)
        op.close()


# insert_size_histogram


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/insert_size_histogram.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("insertSize_hist.csv", "w") as op:
        op.write(mylines)
        op.close()


# mapped_reads_clipping_profile


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/mapped_reads_clipping_profile.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("mappedReads_clip_profile.csv", "w") as op:
        op.write(mylines)
        op.close()


# mapped_reads_gc-content_distribution


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/mapped_reads_gc-content_distribution.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("mappedReads_gc_content_dist.csv", "w") as op:
        op.write(mylines)
        op.close()


# mapped_reads_nucleotide_content


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/mapped_reads_nucleotide_content.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("mappedReads_gc_nucleotide_content.csv", "w") as op:
        op.write(mylines)
        op.close()


# mapping_quality_across_reference


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/mapping_quality_across_reference.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("mappingQuality_ax_ref.csv", "w") as op:
        op.write(mylines)
        op.close()


# mapping_quality_histogram


mylines = ""
col_name = []
row_vals = []

with open ('./txt_files/mapping_quality_histogram.txt') as file:
    for line in file:
        if '#' in line:
            col_name.append(line.replace('\t', ',').replace('#', ''))
        else:
            row_vals.append(line.replace('\t', ','))

for i in col_name:
    mylines += i


for j in row_vals:
    mylines += j

with open("mappingQuality_hist.csv", "w") as op:
        op.write(mylines)
        op.close()