process GATK_VARIANTFILTRATION {
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/gatk:latest'

    input:
    tuple   val(sampleid) , path(vcf), val(vcf_name)
    tuple   path(fasta)   ,path(index)
    path    (logf), stageAs: 'data.ip'
    val     (logname)

    output:
    tuple val(sampleid), path("*_fltred.vcf"), val(vcf_name) ,emit: vcf
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
    echo ">> GATK-VARIANTFILTRATION - LOG FILE" >>data.ip
    gatk --java-options " -Xmx${avail_mem}M -XX:ParallelGCThreads=${task.cpus} " VariantFiltration \\
        -R ${fasta} \\
        -V ${vcf} \\
        -O ${vcf_name}_fltred.vcf \\
        --filter-expression "MQ0 >= 5 && ((MQ0 / (1.0 * DP))) > 0.1" \\
        --filter-name "HARD_TO_VALIDATE"\\
        --filter-expression "DP < 10"\\
        --filter-name "LowCoverage"\\
        --filter-expression "QUAL < 20.0"\\
        --filter-name "VeryLowQual"\\
        --filter-expression "QD < 1.5"\\
        --filter-name "LowQD"\\
        --verbosity ERROR 2>>data.ip

    mv data.ip ${logname}
	"""
}