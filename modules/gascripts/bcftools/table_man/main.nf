process TABLE_MANIPULATE{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/bcftools:latest'

	input:
	tuple 	val(sampleid)	, val(vcf_name),
			path(vcf)		, path(vcf_idx),
			path(all)
    path (logf), stageAs: 'data.ip'
    val  (logname)

	output:
	tuple	val (sampleid), val (vcf_name),
			path ("${vcf_name}_actionable_variants.txt"),
			path ("*header.txt")						,emit: actionables
	tuple 	val (sampleid), val (vcf_name),
			path ("*_uniq_variants.txt")	    		,emit: all
	path ("*")
    path "*.log" , emit: loge

	script:
	"""
    echo ">> CLINICAL-SIG-TABLE-MANUPULATE - LOG FILE" >>data.ip
	# All variants table : Removing Duplicates from all variants table
	sort ${all} | uniq > ${vcf_name}_uniq_variants.txt 2>>data.ip
	awk 'NR==1{print \$1\"\\t\"\$2"\\t\"\$3\"\\t\"\$4\"\\t\"\$5\"\\tGT\\tEFFECT\\tGENE\\tIMPACT\\tHGVS_C\\t\"\$11\"\\t\"\$12\"\\t\"\$13\"\\t\"\$14\"\\t\"\$15;next}{print}' ${vcf_name}_uniq_variants.txt > ${vcf_name}_actionable_variants_us.txt 2>>data.ip
	cat ${vcf_name}_actionable_variants_us.txt | uniq > ${vcf_name}_actionable_variants.txt 2>>data.ip
	#get the file header
	awk \'NR==1{print \$1\"\\t\"\$2"\\t\"\$3\"\\t\"\$4\"\\t\"\$5\"\\tGT\\tEFFECT\\tGENE\\tIMPACT\\tHGVS_C\\t\"\$11\"\\t\"\$12\"\\t\"\$13\"\\t\"\$14\"\\t\"\$15;next}\' ${vcf_name}_uniq_variants.txt > ${vcf_name}_header.txt 2>>data.ip
    mv data.ip ${logname}
	"""
}

	// # Replace genotype values from numbers (e.g. 1/1) to letters (e.g. AA)
	// bcftools query -f '%ID\\t[%TGT]\\n' ${vcf} > ${vcf_name}_gt_8b.txt

	// awk -vOFS="\\t" 'NR==FNR{a[\$1]=\$2; next}{\$6=a[\$2]; print}' ${vcf_name}_gt_8b.txt ${vcf_name}_uniq_variants.txt > ${vcf_name}_gt_replaced_8b.txt

	// # awk -v OFS="\\t" 'NR==FNR{a[\$1]=\$2; next}{\$6=a[\$2]; print}' ${vcf_name}_gt_8b.txt ${vcf_name}_uniq_variants.txt > ${vcf_name}_gt_replaced_8b.txt
	// # sort -V -k1,1 -k2,2 ${vcf_name}_gt_replaced_8b.txt > ${vcf_name}_gt_replaced_8b_sort.txt
	// # awk 'NR==1{print \$1"\\t"\$2"\\t"\$3"\\t"\$4"\\t"\$5"\\tGT\\tEFFECT\\tGENE\\tIMAPCT\\tHGVS_C\\t"\$10"\\t"\$11"\\t"\$12"\\t"\$13"\\t"\$14;next}{print}' ${vcf_name}_gt_replaced_8b_sort.txt > ${vcf_name}_actionable_variants.txt

	// # Step 9 : Get the file header
	// # awk 'NR==1{print \$1"\\t"\$2"\\t"\$3"\\t"\$4"\\t"\$5"\\tGT\\tEFFECT\\tGENE\\tIMAPCT\\tHGVS_C\\t"\$10"\\t"\$11"\\t"\$12"\\t"\$13"\\t"\$14;next}' ${vcf_name}_gt_replaced_8b_sort.txt > ${vcf_name}_header.txt
			// path(gwas),path(gwas_idx)
	// tuple val (sampleid), val (vcf_name), path ("*_uniq_gwas_variants.txt.gz")	,emit: gwas

	// gzip -f ${vcf_name}_uniq_variants.txt
	// # gzip -f ${vcf_name}_uniq_gwas_variants.txt
	// # gzip -f ${vcf_name}_actionable_variants.txt
			// # GWAS variants table : Removing Duplicatesfrom GWAS variants table
            // # zcat ${gwas} | sort | uniq > ${vcf_name}_uniq_gwas_variants.txt

			// echo "CHROM	ID	POS	REF	ALT	CLNSIG	CLNVC	CLNDN	CLNREVSTAT	AF_TGP" >${vcf_name}_header.txt
