process ADDORREPLACEREADGROUPS {
    tag "${sampleid}"
    label 'process_low'
    queue 'low'

    container 'glslabs/gatk:latest'

    input:
    tuple val (sampleid), path(bam)
    tuple path (fasta)  , path(index)
    path (logf), stageAs:'data.ip'
    val  (logname)

    output:
    tuple val (sampleid), path ("*sort.bam"),   path ("*.bai")  , emit: bam ,  optional: true
    tuple val (sampleid), path ("*sort.cram"),  path ("*.cai")  , emit: cram,  optional: true
    path "*.log"                                                , emit: loge

    when:
    task.ext.when == null || task.ext.when

	script:

	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }
    cram = params.cram ?: ""

    def rglb = "${params.rglb}" ? "${params.rglb}" : "lib1"
    def rgpl = "${params.rgpl}" ? "${params.rgpl}" : "ILLUMINA"
    def rgpu = "${params.rgpu}" ? "${params.rgpu}" : "unit1"
    def rgsm = "${params.rgsm}" ? "${params.rgsm}" : ""
    def name = bam.getSimpleName()

    """
    echo ">> GATK-ADDORREPLACEGROUPS - LOG FILE" >>data.ip
    rgsm="${rgsm}"
    if [ -z "\${rgsm}" ]; then
        rgsm=${sampleid}
    fi
    name=${name}

    gatk --java-options " -Xmx${avail_mem}M -XX:ParallelGCThreads=${task.cpus}" \\
        AddOrReplaceReadGroups \\
        -I "${bam}" \\
        -O "${sampleid}.rg.bam" \\
        --RGLB ${rglb} \\
        --RGPL ${rgpl} \\
        --RGPU ${rgpu} \\
        --RGSM \$rgsm \\
		--VERBOSITY ERROR 2>>data.ip

    samtools sort -o ${sampleid}.rg.sort.bam \\
			-T ${sampleid}.rg.sort \\
			-@ ${task.cpus} \\
			${sampleid}.rg.bam 2>>data.ip

    samtools index -@ ${task.cpus} ${sampleid}.rg.sort.bam 2>>data.ip

    # If cram files are wished as output, the run samtools for conversion
    cram=${cram}
    if [[ -n \$cram ]]; then
        samtools view -Ch -T ${fasta} -o ${sampleid}.rg.sort.cram ${sampleid}.rg.sort.bam 2>>data.ip
        rm ${sampleid}.rg.sort.bam
        samtools index ${sampleid}.rg.sort.cram 2>>data.ip
    fi
    mv data.ip ${logname}
	"""
}