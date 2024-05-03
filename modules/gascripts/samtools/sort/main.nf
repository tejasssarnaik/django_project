process SAMTOOLS_SORT {
    tag "${sampleid}"
    label 'process_low'
    queue 'low'

    container 'glslabs/samtools:latest'

    input:
    tuple val(sampleid), path(bam)
    path (logf), stageAs:'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*sort.bam"), emit: bam
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
    """
    echo ">> SAMTOOLS - LOG FILE" >>data.ip
	samtools sort -o ${sampleid}.sort.bam \\
			-T ${sampleid}.sort \\
			-@ ${task.cpus} \\
			${bam} 2>>data.ip

    mv data.ip ${logname}
	"""
}