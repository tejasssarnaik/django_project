process QUALIMAP {
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

	container 'glslabs/qualimap:latest'

	input:
	tuple val(sampleid), path(bam), path(bai)
    path (logf), stageAs: 'data.ip'
	val  (logname)

	output:
	path "*_stats" 	, emit: qmap
    path "*.log" 	, emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
	def name = bam.getSimpleName()

	"""
    echo ">> QUALIMAP - LOG FILE" >>data.ip
	qualimap bamqc \\
		-bam ${bam} \\
		-nt ${task.cpus} \\
		-outdir . \\
		-outformat PDF:HTML \\
		-outfile "${name}" 2>>data.ip
    mv data.ip ${logname}
	"""
}