process FASTQC {
    tag "${params.processid}"
    label 'process_low'
    queue 'low'
    
    // containerOptions '--shm-size 16000000 --ulimit nofile=1280:2560 --ulimit nproc=16:32'
    container 'glslabs/fastqc:latest'

    input:
    path(fastq)

    output:
    path ("*.{html,zip}")   , emit: html


    when:
    task.ext.when == null || task.ext.when
    
    script:
    """
    fastqc --threads $task.cpus $fastq
    """

}