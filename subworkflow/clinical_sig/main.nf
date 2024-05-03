include { SNPSIFT_EXTRACT   }   from '../../modules/gascripts/snpeff/snpsift/extract/'
include { TABLE_MANIPULATE  }   from '../../modules/gascripts/bcftools/table_man/'
// include { ACTIONABLES       }   from '../../modules/gascripts/actionables/'


workflow CLINICAL_SIG{
    take:
    vcf
    log_file
    log_name

    main:

    // Step 7 : Creating a table with required fields
        SNPSIFT_EXTRACT(vcf,log_file,log_name)
        txt     = SNPSIFT_EXTRACT.out.txt
        l1      = SNPSIFT_EXTRACT.out.loge
    // Step 8 : Manupulating the table of variants to get variants of interest
        TABLE_MANIPULATE(txt,l1,log_name)
        act     = TABLE_MANIPULATE.out.actionables
        l2      = TABLE_MANIPULATE.out.loge

        // .collect()
        // act     = acts.groupTuple().view()
    // Step 11 : Actionable variants separation
        // ACTIONABLES(act,l2,log_name)
        // table   = ACTIONABLES.out.table
        // l3      = ACTIONABLES.out.loge

    emit:
    table = act
    galog = l2
}
