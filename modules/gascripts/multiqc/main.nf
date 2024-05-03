process MULTIQC {
    tag "${params.processid}"
    label 'process_single'
    queue 'single'
    
    // containerOptions '--shm-size 16000000 --ulimit nofile=1280:2560 --ulimit nproc=16:32'
    container 'glslabs/multiqc:latest'

    input:
    path (html)
    // path (logf), stageAs: 'data.ip'
    // val  (logname)

    output:
    path "*.html"   , emit: mhtml
    file "*"
    // path "*.log"    , emit: loge

    when:
    task.ext.when == null || task.ext.when

    script:
    """
    multiqc -m fastqc -q -i GeneAssure:GLS \\
                -b GeneAssure:GLS \\
                -n "GA_Multiqc_Report" \\
                --no-megaqc-upload .
    """
}