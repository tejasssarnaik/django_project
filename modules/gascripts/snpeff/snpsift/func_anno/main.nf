process SNPSIFT_FUNC_ANNO{
	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	tuple path(snpeffhg38),path(snpeffhg38_idx)

	output:
	tuple val (sampleid),val (vcf_name), path ("*3.vcf.gz"),path("*3.vcf.gz.tbi")	,emit: vcf

	script:
	"""
	java "-Xmx${avail_mem}G" -jar /opt/snpEff/SnpSift.jar \\
        -v hg38 ${sampleid}_2.vcf > ${sampleid}_3.vcf

	bgzip -f ${vcf_name}_3.vcf
	tabix ${vcf_name}_3.vcf.gz
	rm -r *vcf
	"""	
}