process VCFSTATS {
    tag "${sampleid}"
    label 'process_single'
    queue 'single'
    container 'glslabs/vcfstats:latest'

    // container 'glslabs/glslabs_public:latest'
    containerOptions "-w `pwd`"

    // publishDir "${params.output_dir}/OUTPUT", mode: 'copy', pattern: "*.png"
    
    input:
    tuple val(sampleid), path(vcf), val(name)
    path (logf), stageAs:'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), file ("*.csv"), emit: stats
    path "*.log" , emit: loge


    when:
    task.ext.when == null || task.ext.when

    """
    echo ">> VCFSTATS - LOG FILE" >>data.ip
    vcfstats \\
    --vcf ${vcf} \\
    --outdir . \\
    --formula 'COUNT(1) ~ CONTIG' \\
        'COUNT(1, VARTYPE[snp]) ~ SUBST[A>T,A>G,A>C,T>A,T>G,T>C,G>A,G>T,G>C,C>A,C>T,C>G]' \\
        'AAF ~ CONTIG' \\
        'AAF ~ 1' \\
        'AAF[0.05, 0.95] ~ 1' \\
        'COUNT(1, group=VARTYPE) ~ CHROM' \\
        'COUNT(1, group=VARTYPE) ~ 1' \\
        'COUNT(1, group=GTTYPEs[HET,HOM_ALT]{0}) ~ CHROM' \\
        'MEAN(GQs{0}) ~ MEAN(DEPTHs{0}, group=CHROM)' \\
    --title "Number of variants on each chromosome" \\
        "Number of substitutions of SNPs" \\
        "Allele frequency on each chromosome" \\
        "Overall allele frequency distribution" \\
        "Overall allele frequency distribution (0.05-0.95)" \\
        "Types of variants on each chromosome" \\
        "Types of variants on whole genome" \\
        "Mutant genotypes on each chromosome (${name})" \\
        "GQ vs depth (${name})" \\
    --save 2>>data.ip
    mv data.ip ${logname}
	"""
}
