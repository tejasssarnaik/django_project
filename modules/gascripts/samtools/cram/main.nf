process SAMTOOLS_CRAM {
    tag "${sampleid}"
    label 'process_low'
    queue 'low'

    container 'glslabs/samtools:latest'


    input:
    tuple val(sampleid), path(bam)
    tuple path(fasta), path(index)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.cram"),path("*.crai"), emit: bam
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
    """
    echo ">> SAMTOOLS - LOG FILE" >>data.ip
    samtools view -T $fasta -C -o ${sampleid}.cram ${bam} 2>>data.ip
    mv data.ip ${logname}
	"""
}