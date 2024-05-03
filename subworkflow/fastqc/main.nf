include {FASTQC_SCRIPT} from '../../modules/gascripts/fastqc/main.nf'

workflow FASTQC {
    take:
    fastq

    main:
    
    FASTQC_SCRIPT(fastq)
    
    op = FASTQC_SCRIPT.out.html

    emit:
    html = op
}