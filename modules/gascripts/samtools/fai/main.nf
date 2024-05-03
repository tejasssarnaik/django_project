process SAMTOOLS_FAI {
    tag "${fasta}"
    label 'process_low'
    queue 'low'

    container 'glslabs/samtools:latest'


    input:
    path(fasta)

    output:
    tuple path("*.fasta"),path("*.fai"), emit: fai

    when:
    task.ext.when == null || task.ext.when

	script:
    """
	samtools faidx -@ ${task.cpus} ${fasta}
	"""
}