process GATK_HAPLOTYPECALLER {
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/gatk:latest'

    input:
    tuple val(sampleid), path(bam), path(bai)
    tuple path(fasta),path(index)
    path    (intervalList)
    path    (logf), stageAs: 'data.ip'
    val     (logname)

    output:
    tuple val(sampleid), path("*vcf"), val("${sampleid}.gavcf1") ,emit: gavcf1
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
    echo ">> GATK-HAPLOTYPECALLER - LOG FILE" >>data.ip
    gatk --java-options " -Xmx${avail_mem}M -XX:ParallelGCThreads=${task.cpus}" \\
        HaplotypeCaller \\
        -L ${intervalList} \\
        -R ${fasta} \\
        -I ${bam} \\
        -O ${sampleid}.gavcf1.vcf \\
        --verbosity ERROR 2>>data.ip

    mv data.ip ${logname}
	"""
}