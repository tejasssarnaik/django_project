process SNPSIFT_FILTER_S6{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/snpeff:latest'

	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	path (logf), stageAs:'data.ip'
    val  (logname)

	output:
	tuple 	val (sampleid),
			val (vcf_name),
			path ("${vcf_name}_variants_in_dbsnp.vcf.gz"),
			path ("${vcf_name}_variants_in_dbsnp.vcf.gz.tbi"),
			path ("${vcf_name}_variants_in_dbsnp_AF.vcf.gz"),
			path ("${vcf_name}_variants_in_dbsnp_AF.vcf.gz.tbi"),

			emit: vcf

	path ("*")
    path "*.log" , emit: loge

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }
	"""
    echo ">> VCF-ANNOTATION-FILTER - LOG FILE" >>data.ip

	java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar filter \\
			-f ${vcf} "exists ID" > ${vcf_name}_variants_in_dbsnp.vcf 2>>data.ip

	java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar filter \\
		-f ${vcf} "!exists ID" > ${vcf_name}_variants_NO_dbsnp_RSID.vcf 2>>data.ip

	java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar filter "(AF_TGP >= 0.01)" \\
			-f ${vcf} > ${vcf_name}_variants_in_dbsnp_AF.vcf 2>>data.ip

	bgzip -f ${vcf_name}_variants_in_dbsnp.vcf
	tabix ${vcf_name}_variants_in_dbsnp.vcf.gz
	bgzip -f ${vcf_name}_variants_NO_dbsnp_RSID.vcf
	tabix ${vcf_name}_variants_NO_dbsnp_RSID.vcf.gz
	bgzip -f ${vcf_name}_variants_in_dbsnp_AF.vcf
	tabix ${vcf_name}_variants_in_dbsnp_AF.vcf.gz

    mv data.ip ${logname}.log
	"""
}