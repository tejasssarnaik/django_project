process BWA_MEM {
    tag "${sampleid}"
    label 'process_high'
    queue 'high'

    container 'glslabs/bwa:latest'

    input:
    tuple val(sampleid), path(read1), path(read2)
    tuple path(fasta), path(index)
    // path (logf), stageAs: 'data.ip'
    // val  (logname)

    output:
    tuple val(sampleid), path("*.bam")  , emit: bam
    path ("*.log")                      , emit: loge
    env  LOG_NAME                       , emit: log_name

    when:
    task.ext.when == null || task.ext.when

	script:
    if ("${params.paired}"){
    """
    current_time=\$(date "+%Y%m%d%H%M_%S")
    LOG_NAME="\${current_time}.log"
    touch \${current_time}.log

    echo ">> BWA-MEM - LOG FILE" >>\$LOG_NAME
	bwa mem -v 1 -t ${task.cpus} \\
            ${fasta} \\
			${read1} \\
            ${read2} > ${sampleid}.bam 2>>\$LOG_NAME
	"""
    }
    else {
    """
    current_time=\$(date "+%Y%m%d%H%M_%S")
    LOG_NAME=\${current_time}.log
    touch \${current_time}.log

    echo ">> BWA-MEM - LOG FILE" >>\$LOG_NAME
	bwa mem -v 1 -t ${task.cpus} \\
            ${fasta} \\
			${read1} > ${sampleid}.bam \$LOG_NAME
	"""
    }
}