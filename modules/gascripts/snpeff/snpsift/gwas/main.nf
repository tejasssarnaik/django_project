process SNPSIFT_GWAS{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/snpeff:latest'

	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	tuple path(gwas),path(gwas_idx)
	path (logf), stageAs:'data.ip'
    val  (logname)

	output:
	tuple val (sampleid), val (vcf_name), path ("*5.vcf.gz"), path ("*5.vcf.gz.tbi")	,emit: vcf
    path "*.log"                                                						, emit: loge

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }
	"""
    echo ">> VCF-ANNOTATION-GWAS - LOG FILE" >>data.ip

	java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar gwasCat\\
		-db ${gwas} ${vcf_name}_4.vcf > ${vcf_name}_5.vcf 2>>data.ip

	bgzip -f ${vcf_name}_5.vcf
	tabix ${vcf_name}_5.vcf.gz

    mv data.ip ${logname}.log
	"""
}