include { DEEPVARIANT }     from '../../modules/gascripts/deepvariant/main.nf'

workflow DEEPVARIANT_WF {
    take:
    bam
    fasta_index
    intervalList

    main:
    DEEPVARIANT(bam,fasta_index,intervalList)
    op = DEEPVARIANT.out.gavcf2
    emit:
    vcf = op
}