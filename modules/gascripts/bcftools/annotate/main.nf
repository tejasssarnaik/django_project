process BCFTOOLS_ANNOTATE{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/bcftools:latest'

	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	tuple path(dbsnp), path(dbsnp_idx)
	path (logf), stageAs:'data.ip'
    val  (logname)

	output:
	tuple val (sampleid), val (vcf_name), path ("*2.vcf.gz"), path ("*2.vcf.gz.tbi")	, emit: vcf 
    path "*.log"                                                						, emit: loge

	script:
	"""
    echo ">> VCF-ANNOTATION-S2 - LOG FILE" >>data.ip

	bcftools annotate -a ${dbsnp} \\
			-c ID ${vcf} \\
			-o ${vcf_name}_2.vcf \\
			--threads ${task.cpus} 2>>data.ip

	bgzip -f ${vcf_name}_2.vcf
	tabix ${vcf_name}_2.vcf.gz
    mv data.ip ${logname}.log
	"""
}