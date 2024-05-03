include { BWA_MEM }   from '../../modules/gascripts/bwa/mem/main.nf'

workflow MAPPING {
    take:
    fastq
    fasta_index
    // logf
    // log_name
    
    main:
    BWA_MEM(fastq,fasta_index) //,logf,log_name)
    op      = BWA_MEM.out.bam
    log1    = BWA_MEM.out.loge
    galogn  = BWA_MEM.out.log_name

    emit:
    bam     = op
    galog   = log1
    galogn
}