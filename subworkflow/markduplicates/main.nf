include { ADDORREPLACEREADGROUPS    }  from '../../modules/gascripts/gatk/addorreplacegroups/'
include { MARKDUPLICATES            }  from '../../modules/gascripts/gatk/markduplicates/'
include { BASERECALIBRATOR          }  from '../../modules/gascripts/gatk/baserecalibrator/'
include { APPLYBQSR                 }  from '../../modules/gascripts/gatk/applybqsr/'
include { SAMTOOLS_STATS            }  from '../../modules/gascripts/samtools/stats/'
include { QUALIMAP                  }  from '../../modules/gascripts/qualimap/'

workflow GATK_MARKDUPLICATES {
    take:
    bam
    fasta_index
    snp_index
    indel_index
    logf
    log_name

    main:

    ADDORREPLACEREADGROUPS( bam,fasta_index,logf,log_name )
    rgbam   = ADDORREPLACEREADGROUPS.out.bam
    log1     = ADDORREPLACEREADGROUPS.out.loge

    MARKDUPLICATES( rgbam,log1,log_name )
    mkbam   = MARKDUPLICATES.out.bam
    mdfile  = MARKDUPLICATES.out.md
    op      = mkbam.join(mdfile)
    log2    = MARKDUPLICATES.out.loge

    SAMTOOLS_STATS(mkbam,log2,log_name)
    log3    = SAMTOOLS_STATS.out.loge

    QUALIMAP(mkbam,log3,log_name)
    log4    = QUALIMAP.out.loge

    emit:
    bam     = op
    galog   = log4
}