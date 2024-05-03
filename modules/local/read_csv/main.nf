process READ_CSV {

    input:

    output:
    tuple val(sampleid),path(fastq),        emit: fastq
    tuple val(sampleid),path(bam),          emit: bam
    path(ref_fasta),path(fai),path(dict)    emit: fasta
    path(snp),path(snp_tbi)                 emit: snp
    path(indel),path(indel_tbi)             emit: indel
}