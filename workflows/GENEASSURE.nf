include { FASTQ_QUAL_CHECK      } from '../subworkflow/fastq_qual_check/'
include { FASTP                 } from '../subworkflow/fastp/'
include { MAPPING               } from '../subworkflow/mapping/'
include { GATK_MARKDUPLICATES   } from '../subworkflow/markduplicates/'
include { GATK_APPLYBQSR        } from '../subworkflow/applybqsr/'
include { DEEPVARIANT_WF        } from '../subworkflow/deepvariant/'
include { VARIANT_CALLING       } from '../subworkflow/variant_calling/'
include { VCF_ANNOTATION        } from '../subworkflow/annotation/'
include { CLINICAL_SIG          } from '../subworkflow/clinical_sig/'

// Define a function to extract file information and create index channel

def createIndexChannel(fileParam) {
    file        = file(fileParam, checkIfExists:true)
    fileName    = file.getName()
    fileDir     = file.getParent().toUriString()
    fileIndex   = file("${fileDir}/${fileName}.{tbi,idx}", checkIfExists:true)
    return Channel.from(file, fileIndex).collect()
}

workflow GENEASSURE {
    /**********
    Inititalizing all required variables and files
    **********/
    // Declaring channels
    csv             = Channel.empty()
    only_fq         = Channel.empty()
    fastq           = Channel.empty()
    fasta_index1    = Channel.empty()
    fasta_index2    = Channel.empty()
    snp_index       = Channel.empty()
    indel_index     = Channel.empty()
    snp_indel       = Channel.empty()
    only_fq         = Channel.empty()
    fastq           = Channel.empty()
    dbsnp_index     = Channel.empty()
    gwas_index      = Channel.empty()
    clinvar_index   = Channel.empty()
    dbnsfp          = Channel.empty()
    intervalList_file = Channel.empty()
    bed             = Channel.empty()

    /**********
    GENEASSURE INPUTS
    **********/
    // Collecting csv files
    csv             = file( params.csv, checkIfExists: true )
    // Only FASTQ as input
    only_fq         = Channel
                        .fromPath(csv)
                        .splitCsv(header:true, strip:true)
                        .flatMap{ row-> tuple(row.FASTQ1,row.FASTQ2) }.collect()
    // Sampleid,FASTQ as input
    fastq           = Channel
                        .fromPath(csv)
                        .splitCsv(header:true, strip:true)
                        .map{ row-> tuple(row.SAMPLEID,file(row.FASTQ1),file(row.FASTQ2)) }

    // Collecting fasta and fasta index files
    ref_genome      = file( params.fasta, checkIfExists: true )
    ref_dir         = ref_genome.getParent().toUriString()
    ref_name        = ref_genome.getBaseName()
    ref_dict        = file( "${ref_dir}/${ref_name}.dict", checkIfExists: true )
    ref_index       = file( "${ref_dir}/${ref_name}.{fa,fna,fasta}.{ann,amb,bwt,fai,pac,sa}", checkIfExists: true )
    fasta_index1    = Channel.from(ref_genome).toList()
    fasta_index2    = Channel.from(ref_dict,ref_index).collect().toList()
    fasta_index     = fasta_index1.mix(fasta_index2).collect()

    // Use the function to create channels for GWAS, CLINVAR, and dbNSFP
    snp_index       = createIndexChannel(params.snp)
    indel_index     = createIndexChannel(params.indel)
    // dbsnp_index     = createIndexChannel(params.dbsnp)
    // gwas_index      = createIndexChannel(params.gwas)
    // clinvar_index   = createIndexChannel(params.clinvar)

    // Collecting INTERVALS LIST files
    intervalList_file   = params.intervalList
    bed             = params.bed


    /**********
    GENEASSURE MAIN WORKFLOW
    **********/


    /* RUN PROCESSES */

    //STEP1: FASTQ QUALITY CHECK
    FASTQ_QUAL_CHECK(only_fq)

    //STEP2: FASTQ TRIMMING
    trim    = params.trim
    trim    = trim.toLowerCase()

    if      ( trim.contains("true") ) {
        FASTP( fastq )
    }
    else if ( trim.contains("false") ) {
        println "${params.RED}'--trim' is '${trim}', Skipping trimming${params.CLEAR}"
    }
    else if ( trim == "" ) {
        println "${params.RED}'--trim' is empty, Skipping trimming${params.CLEAR}"        
    }
    else {
        println "${params.RED}'--trim' have invalid value '${trim}', Skipping trimming${params.CLEAR}"
    }


    if (params.skip_steps && params.skip_steps.split(',').contains('mapping')) {
        bam = Channel
                .fromPath(csv)
                .splitCsv(header:true, strip:true)
                .map{ row-> tuple(row.SAMPLEID,file(row.BAM)) }
    } else {
        // MAPPING BWA-MEM
        MAPPING(fastq,fasta_index)
        bam         = MAPPING.out.bam
        log2        = MAPPING.out.galog
        log_name    = MAPPING.out.galogn
    }

    // // test-temp-vals
    // log2     = "${params.galog}"
    // log_name = "vcf_anno_test.log"

    // MARK DUPLICATES
    GATK_MARKDUPLICATES(bam,
                fasta_index,
                snp_index,
                indel_index,
                log2,
                log_name)

    bamp    = GATK_MARKDUPLICATES.out.bam
    log3    = GATK_MARKDUPLICATES.out.galog

    // APPLY BQSR
    GATK_APPLYBQSR(bamp,
                fasta_index,
                snp_index,
                indel_index,
                log3,
                log_name)

    bamf    = GATK_APPLYBQSR.out.bam
    log4    = GATK_APPLYBQSR.out.galog

    // VARIANT_CALLING(BOTH)
    VARIANT_CALLING(bamf,
                fasta_index,
                intervalList_file,
                bed,
                log4,
                log_name)

    vcfs1   = VARIANT_CALLING.out.vcf1
    log5    = VARIANT_CALLING.out.galog



    // VCF_ANNOTATION

    // FOR TESTING SCRIPT
    // log5    = log2
    // vcfs1   = Channel
    //         .fromPath("${params.vcf}")
    //         .splitCsv(header:true, strip:true)
    //         .flatMap{ row-> tuple(row.SAMPLEID,row.VCF,row.VCF_NAME) }.collect()

    // VCF_ANNOTATION(vcfs1,
    //             fasta_index,
    //             dbsnp_index,
    //             clinvar_index,
    //             gwas_index,
    //             log5,
    //             log_name)

    // vcfs2   = VCF_ANNOTATION.out.vcf
    // log6    = VCF_ANNOTATION.out.galog

    // // EXTRACTING CLINICAL_SIGNIFICANCE
    // CLINICAL_SIG(vcfs2,log6,log_name)
    // tables = CLINICAL_SIG.out.table
}