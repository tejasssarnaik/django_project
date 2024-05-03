process BCFTOOLS_STATS {
    tag "${sampleid}"
    label 'process_single'
    queue 'single'

    container 'glslabs/bcftools:latest'

    input:
    tuple val(sampleid), path(vcf), val(name)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.txt"), emit: stats
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
    """
    echo ">> BCFTOOLS-STATS - LOG FILE" >>data.ip
	bcftools stats --threads ${task.cpus} ${vcf} \\
		> ${name}.stats.txt 2>>data.ip
    mv data.ip ${logname}
	"""
}