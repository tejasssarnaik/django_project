process SAMTOOLS_STATS {
    tag "${sampleid}"
    label 'process_low'
    queue 'low'

    container 'glslabs/samtools:latest'

    input:
    tuple val(sampleid), path(bam), path(bai)
    path (logf), stageAs:'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.txt"), emit: stats
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
    def name = bam.getSimpleName()
    """
    echo ">> SAMTOOLS - LOG FILE" >>data.ip
	samtools stats -@ ${task.cpus} ${bam} \\
		> ${name}.stats.txt 2>>data.ip
    mv data.ip ${logname}
	"""
}