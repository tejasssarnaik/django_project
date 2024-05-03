include { GATK_VARIANTFILTRATION}   from '../../modules/gascripts/gatk/variantfiltration/'
include { SNPSIFT_FILTER_PASS   }   from '../../modules/gascripts/snpeff/snpsift/filter/S1/'
include { BCFTOOLS_ANNOTATE     }   from '../../modules/gascripts/bcftools/annotate/'
include { SNPEFF_FUNC_ANNO      }   from '../../modules/gascripts/snpeff/snpeff/'
include { VCFANNO               }   from '../../modules/gascripts/vcfanno/'
include { SNPSIFT_GWAS          }   from '../../modules/gascripts/snpeff/snpsift/gwas/'
include { SNPSIFT_DBNSFP        }   from '../../modules/gascripts/snpeff/snpsift/dbnsfp/'
include { SNPSIFT_FILTER_S6     }   from '../../modules/gascripts/snpeff/snpsift/filter/S6/'
include { SNPSIFT_CLINVAR       }   from '../../modules/gascripts/snpeff/snpsift/annotate/'

/* VCF Annotation */
workflow VCF_ANNOTATION {
    take:
	vcf_files
    fasta
    dbsnp
	clinvar
	gwas
    logf
    log_name

    main:

	// Step 1 : Quality parameter filtering
        GATK_VARIANTFILTRATION(vcf_files,fasta,logf,log_name)
        v0 = GATK_VARIANTFILTRATION.out.vcf
        l0   = GATK_VARIANTFILTRATION.out.loge

	// Step 2 : Quality parameter filtering
        SNPSIFT_FILTER_PASS(v0,l0,log_name)
        v1 = SNPSIFT_FILTER_PASS.out.vcf
        l1 = SNPSIFT_FILTER_PASS.out.loge

    // // Step 2 : Adding dbSNP Ids to variants
    //     BCFTOOLS_ANNOTATE(v1,dbsnp,l1,log_name)
    //     v2 = BCFTOOLS_ANNOTATE.out.vcf
    //     l2 = BCFTOOLS_ANNOTATE.out.loge

    // // // Step 3 : Clinvar Annotation
    //     SNPSIFT_CLINVAR(v1,clinvar,l1,log_name)
    //     v3 = SNPSIFT_CLINVAR.out.vcf
    //     l3 = SNPSIFT_CLINVAR.out.loge

    // Step 4 : Clinvar Annotation
        VCFANNO(v1,clinvar,l1,log_name)
        v3 = VCFANNO.out.vcf
        l3 = VCFANNO.out.loge

    // Step 4 : Functional annotation with SnpEff on GRCh38
        SNPEFF_FUNC_ANNO(v3,l3,log_name)
        v4 = SNPEFF_FUNC_ANNO.out.vcf
        l4 = SNPEFF_FUNC_ANNO.out.loge


    // // Step 5 : Annotating variants with GWAS Catalog
    //     SNPSIFT_GWAS(v4,gwas,l4,log_name)
    //     v5 = SNPSIFT_GWAS.out.vcf
    //     l5 = SNPSIFT_GWAS.out.loge

    // // Step 6 : Annotating variants with dbNSFP Catalog
    //     SNPSIFT_DBNSFP(v5,l5,log_name)
    //     v6 = SNPSIFT_DBNSFP.out.vcf
    //     l6 = SNPSIFT_DBNSFP.out.loge

    // Step 7 : Post Annotation filtering
        SNPSIFT_FILTER_S6(v4,l4,log_name)
        v7 = SNPSIFT_FILTER_S6.out.vcf
        l7 = SNPSIFT_FILTER_S6.out.loge

    emit:
	vcf     = v7
    galog   = l7
}