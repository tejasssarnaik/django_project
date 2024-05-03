include {FASTQC}     from '../../modules/gascripts/fastqc/main.nf'
include {MULTIQC}    from '../../modules/gascripts/multiqc/main.nf'

workflow FASTQ_QUAL_CHECK {
    take:
    fastq

    main:
    FASTQC(fastq)
    html     = FASTQC.out.html

    MULTIQC(html)
    mhtml = MULTIQC.out.mhtml

    emit:
    html    = mhtml
}