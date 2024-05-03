process SNPSIFT_DBNSFP{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/snpeff:latest'
    containerOptions "-v ${params.dbnsfp}:./data"

	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	path (logf), stageAs:'data.ip'
    val  (logname)

	output:
	tuple val (sampleid), env (vcf_name), path ("*_dbnsfp.vcf.gz"), path ("*_dbnsfp.vcf.gz.tbi")	, emit: vcf 
    path "*.log"                                                									, emit: loge

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }
	"""
    echo ">> VCF-ANNOTATION-S6 - LOG FILE" >>data.ip

    java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar dbnsfp \\
        -v ${vcf} > ${vcf_name}_dbnsfp.vcf 2>>data.ip

	bgzip -f ${vcf_name}_dbnsfp.vcf
	tabix ${vcf_name}_dbnsfp.vcf.gz
	rm -r *vcf
    mv data.ip ${logname}.log
	"""
}

