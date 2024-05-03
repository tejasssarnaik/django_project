process APPLYBQSR {
    tag "${sampleid}"
    label 'process_low'
    queue 'low'
    
    container 'glslabs/gatk:latest'

    input:
    tuple val(sampleid), path(bam), path(br_table)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.bam"), path("*bam.bai"), emit: bam
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
    echo ">> GATK-APPLYBQSR - LOG FILE" >>data.ip
	gatk --java-options " -Xmx${avail_mem}M -XX:ParallelGCThreads=${task.cpus}" \\
        ApplyBQSR \\
		-bqsr ${br_table} \\
		-I ${bam} \\
		-O ${sampleid}.ga_processed.bam \\
		--verbosity ERROR 2>>data.ip

    samtools index ${sampleid}.ga_processed.bam 2>>data.ip
    mv data.ip ${logname}
	"""
}