include { BASERECALIBRATOR  }   from '../../modules/gascripts/gatk/baserecalibrator/'
include { APPLYBQSR         }   from '../../modules/gascripts/gatk/applybqsr/'
include { SAMTOOLS_STATS    }   from '../../modules/gascripts/samtools/stats/'
include { QUALIMAP          }   from '../../modules/gascripts/qualimap/'

workflow GATK_APPLYBQSR {
    take:
    bam
    fasta_index
    snp_index
    indel_index
    logf
    log_name

    main:
    BASERECALIBRATOR( bam, fasta_index, snp_index, indel_index,logf,log_name )
    br_table = BASERECALIBRATOR.out.bam
    log1     = BASERECALIBRATOR.out.loge

    APPLYBQSR( br_table,log1,log_name )
    op      = APPLYBQSR.out.bam
    log2    = APPLYBQSR.out.loge

    SAMTOOLS_STATS(op,log2,log_name)
    log3    = SAMTOOLS_STATS.out.loge

    QUALIMAP(op,log3,log_name)
    log4    = QUALIMAP.out.loge

    emit:
    bam     = op
    galog   = log4
}