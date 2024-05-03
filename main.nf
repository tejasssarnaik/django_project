/*************************************** 
    Main script for running ASE-Analysis
****************************************/
nextflow.enable.dsl=2

include { GENEASSURE } from './workflows/GENEASSURE.nf'
log.info """\
    ${params.RED}===========================================
            G E N E A S S U R E
    ===========================================${params.CLEAR}
    ${params.PURPLE}-input directory    = ${params.YELLOW}${params.ipdir}
    ${params.PURPLE}-output directory   = ${params.YELLOW}${params.output_dir}
    ${params.PURPLE}-input sample csv   = ${params.YELLOW}${params.csv}
    ${params.PURPLE}-reference fasta    = ${params.YELLOW}${params.fasta}
    ${params.PURPLE}-reference snp      = ${params.YELLOW}${params.snp}
    ${params.PURPLE}-reference indel    = ${params.YELLOW}${params.indel}
    ${params.PURPLE}-interval list      = ${params.YELLOW}${params.intervalList}
    ${params.PURPLE}-max_memory         = ${params.YELLOW}${params.max_memory}
    ${params.PURPLE}-max_cpus           = ${params.YELLOW}${params.max_cpus}
    ${params.PURPLE}-max_time           = ${params.YELLOW}${params.max_time}
    ${params.PURPLE}-skip_steps         = ${params.YELLOW}${params.skip_steps}
    ${params.PURPLE}-skip_tools         = ${params.YELLOW}${params.skip_tools}
    ${params.RED}===========================================
        W O R K F L O W - S U M M A R Y
    ===========================================${params.CLEAR}
    ${params.CYAN}-launchDir    = ${params.BLUE}$workflow.launchDir
    ${params.CYAN}-workDir      = ${params.BLUE}$workflow.workDir
    ${params.CYAN}-projectDir   = ${params.BLUE}$workflow.projectDir
    ${params.CYAN}-userName     = ${params.BLUE}$workflow.userName
    ${params.CYAN}-config       = ${params.BLUE}$workflow.configFiles
    ${params.CYAN}-container    = ${params.BLUE}$workflow.container
    ${params.CYAN}-profile      = ${params.BLUE}$workflow.profile${params.CLEAR}
    ${params.RED}===========================================${params.CLEAR}
    """
    .stripIndent()

workflow {

    GENEASSURE ()
}

workflow.onComplete {
    if ( workflow.success ) {
log.info """\
\n${params.CYAN}[$workflow.manifest.name]${params.GREEN}SUCCESSFULLY COMPLETED.\nEXE TIME:$workflow.duration\n${params.CLEAR}
"""
.stripIndent()

    } else {
log.info """\
\n${params.CYAN}[$workflow.manifest.name]${params.RED}:ERROR \n$workflow.duration\nEXE TIME:[$workflow.manifest.name]${params.CLEAR}
"""
.stripIndent()
    }
}