process MARKDUPLICATES {
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/gatk:latest'

    input:
    tuple val(sampleid), path(bam), path(bai)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.mk.bam"), path("*.mk.bam.bai") , emit: bam
    tuple val(sampleid), path("*.md.txt")                       , emit: md
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }

    """
    echo ">> GATK-MARKDUPLICATES - LOG FILE" >>data.ip
    gatk --java-options " -Xmx${avail_mem}M -XX:ParallelGCThreads=${task.cpus}" \\
        MarkDuplicates \\
        -I ${bam} \\
        -M ${sampleid}.md.txt \\
        -O ${sampleid}.rg.sort.mk.bam \\
        --VERBOSITY ERROR 2>>data.ip

    samtools index -@ ${task.cpus} ${sampleid}.rg.sort.mk.bam 2>>data.ip
    mv data.ip ${logname}
	"""
}