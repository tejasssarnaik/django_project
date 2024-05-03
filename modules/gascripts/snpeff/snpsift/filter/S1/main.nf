process SNPSIFT_FILTER_PASS{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/snpeff:latest'

	input:
	tuple val(sampleid), path(vcf), val(vcf_name)
	path (logf), stageAs:'data.ip'
    val  (logname)


	output:
	tuple val (sampleid), val (vcf_name), path ("*_1.vcf.gz"), path ("*_1.vcf.gz.tbi")	, emit: vcf 
    path "*.log"                                                						, emit: loge

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }
	"""
    echo ">> VCF-ANNOTATION-PASS - LOG FILE" >>data.ip
	
	java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar filter \\
			"(FILTER = 'PASS')" -verbose -noLog \\
			${vcf} > ${vcf_name}_1.vcf 2>>data.ip

	bgzip -f ${vcf_name}_1.vcf
	tabix ${vcf_name}_1.vcf.gz
	rm -r *vcf
    mv data.ip ${logname}.log
	"""
}