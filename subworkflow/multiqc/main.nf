include {MULTIQC_SCRIPT} from '../../modules/gascripts/multiqc/main.nf'

workflow MULTIQC {
    take:
    html
    logf
    log_name

    main:
    MULTIQC_SCRIPT(html,logf,log_name)
    log1 = MULTIQC_SCRIPT.out.loge

    emit:
    log = log1
}