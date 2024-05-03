include { GATK_HAPLOTYPECALLER  }     from '../../modules/gascripts/gatk/haplotypecaller/'
include { DEEPVARIANT           }     from '../../modules/gascripts/deepvariant/'
include { BCFTOOLS_STATS        }     from '../../modules/gascripts/bcftools/stats/'
include { VCFSTATS              }     from '../../modules/gascripts/vcfstats/'

workflow VARIANT_CALLING {
    take:
    bam
    fasta_index
    intervalList
    bed
    logf
    log_name

    main:
    GATK_HAPLOTYPECALLER(bam,fasta_index,intervalList,logf,log_name)
    op1     = GATK_HAPLOTYPECALLER.out.gavcf1
    log1    = GATK_HAPLOTYPECALLER.out.loge

    DEEPVARIANT(bam,fasta_index,bed,logf,log_name)
    op2     = DEEPVARIANT.out.gavcf2
    log2    = DEEPVARIANT.out.loge

    vcfs    = op1.mix(op2)
    BCFTOOLS_STATS(vcfs,logf,log_name)
    stats1   = BCFTOOLS_STATS.out.stats
    log3    = BCFTOOLS_STATS.out.loge

    VCFSTATS(vcfs,log3,log_name)
    stats2  = VCFSTATS.out.stats
    log4    = VCFSTATS.out.loge

    emit:
    vcf1    = op1
    vcf2    = op2
    galog   = log4
    stats1
    stats2
}