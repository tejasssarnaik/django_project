include {FASTP_SCRIPT} from '../../modules/gascripts/fastp/main.nf'

workflow FASTP {
    take:
    fastq

    main:
    FASTP_SCRIPT(fastq)
    op  = FASTP_SCRIPT.out.trimmed

    emit:
    trimmed = op

}