process DEEPVARIANT {
	tag "${sampleid}"
	label "process_high"
    queue 'high'

    container 'glslabs/deepvariant:latest'

	input:
	tuple val(sampleid), path(bam), path(bai)
	tuple path(fasta), path(index)
	path (intervalList)
    path (logf), stageAs: 'data.ip'
	val (logname)

	output:
	tuple val("${sampleid}"), path("*gavcf2.vcf"), val("${sampleid}.gavcf2")	, emit : gavcf2
	path ("{${sampleid}_gavcf2,*visual_report.html}")
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
	def sequencing_type = params.sequencing_type ?: "WES"
	def dryrun 			= params.dryrun ?: "false"

	"""
    echo ">> DEEPVARIANT - LOG FILE" >>data.ip
	/opt/deepvariant/bin/run_deepvariant \\
		--model_type=${sequencing_type} \\
		--ref=${fasta} \\
		--regions=${intervalList} \\
		--reads=${bam} \\
		--output_vcf="${sampleid}.gavcf2.vcf" \\
		--num_shards=${task.cpus} \\
		--logging_dir="${sampleid}_gavcf2" \\
		--dry_run=${dryrun} 2>>data.ip
	mv data.ip ${logname}
	"""

	stub:
	"""
	touch ${bam}.gavcf2.vcf
	touch ${bam}.visual_report.html
	"""
}
