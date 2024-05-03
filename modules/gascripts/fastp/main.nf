process FASTP_SCRIPT {
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/fastp:latest'
    input:
    tuple val(sampleid),path(fastq1),path(fastq2)

    output:
    tuple val("${sampleid}"), path("trimmed1_*"), path("trimmed2_*"), emit: trimmed
    path("*.html")
    path("*.json")

    when:
    task.ext.when == null || task.ext.when

    script:
    def paired = params.paired

    if (paired) {
    """
    fastp --in1 "${fastq1}" \\
        --out1 "trimmed1_${fastq1}" \\
        --in2 "${fastq2}" \\
        --out2 "trimmed2_${fastq2}" \\
        --json "${sampleid}.fastp.json" \\
        --html "${sampleid}.fastp.html" \\
        --report_title 'GLS:GeneAssure:${sampleid}' \\
        -p -w $task.cpus
    """
    } else {
    """
    fastp --in1 "${fastq1}" \\
        --out1 "trimmed1_${fastq1}" \\
        --json "${sampleid}.fastp.json" \\
        --html "${sampleid}.fastp.html" \\
        --report_title 'GLS:GeneAssure:${sampleid}' \\
        -p \\
        -w $task.cpus
    """
    }
}