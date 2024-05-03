process BASERECALIBRATOR {
    tag "${sampleid}"
    label 'process_low'
    label 'process_low'
    queue 'low'
    container 'glslabs/gatk:latest'

    input:
    tuple val (sampleid) , path(bam) , path(bai), path(md)
    tuple path (fasta)   , path(index)
    tuple path (snp)     , path(snpidx)
    tuple path (indel)   , path(indelidx)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*.br.bam"), path("*BR.table"), emit: bam
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
    def name = bam.getSimpleName()
    """
    echo ">> BASERECALIBRATOR - LOG FILE" >>data.ip
	gatk --java-options " -Xmx${avail_mem}M " \\
        BaseRecalibrator \\
		-I ${bam} \\
        --known-sites ${snp} \\
        --known-sites ${indel} \\
		-O ${name}.BR.table \\
		-R ${fasta} \\
		--verbosity ERROR 2>>data.ip

    mv ${bam} ${name}.br.bam
    mv data.ip ${logname}
	"""
}