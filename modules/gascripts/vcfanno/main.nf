process VCFANNO{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/vcfanno:latest'

	input:
	tuple val(sampleid),val(vcf_name), path(vcf),path(vcf_idx)
	tuple path(clinvar),path(clinvar_idx)
	path (logf), stageAs:'data.ip'
    val  (logname)

	output:
	tuple val (sampleid),val (vcf_name), path ("*4.vcf.gz"),path("*4.vcf.gz.tbi")	, emit: vcf
    path "*.log"                                                					, emit: loge

	script:
	"""
    echo ">> VCF-ANNOTATION-S4 - LOG FILE" >>data.ip

	vcfanno -p ${task.cpus} \\
		-lua /opt/clinvar_sig.lua \\
		/opt/conf.toml \\
		${vcf} > ${vcf_name}_4.vcf 2>>data.ip

	bgzip -f ${vcf_name}_4.vcf
	tabix ${vcf_name}_4.vcf.gz

    mv data.ip ${logname}.log
	"""
}