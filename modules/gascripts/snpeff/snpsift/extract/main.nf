process SNPSIFT_EXTRACT{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/snpeff:latest'

	input:
	tuple   val(sampleid),
            val(vcf_name), 
            path(dbsnp),path(dbsnp_idx),
            path(dbsnp_af),path(dbsnp_af_idx)
    path (logf), stageAs: 'data.ip'
    val  (logname)

	output:
	tuple   val (sampleid)  , val (vcf_name),
            path("*_final.vcf.gz")  , path ("*_final.vcf.gz.tbi"),
            path("*_all_var_table.txt")                             , emit: txt
    path "*.log" , emit: loge

	script:
	def avail_mem = 3072
    if (!task.memory) {
        log.info '[GATK MarkDuplicates] Available memory not known - defaulting to 3GB. Specify process memory requirements to change this.'
    } else {
        avail_mem = (task.memory.mega*0.8).intValue()
    }

	"""
    echo ">> CLINICAL-SIG-EXTRACT - LOG FILE" >>data.ip
    zcat ${dbsnp_af} \\
        | /app/snpEff/scripts/vcfEffOnePerLine.pl \\
        | java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar extractFields - CHROM ID POS REF ALT \"GEN[*].GT\" \"ANN[*].EFFECT\" \"ANN[*].GENE\" \"ANN[*].IMPACT\" \"ANN[*].HGVS_C\" CLNSIG CLNVC CLNDN CLNREVSTAT AF_TGP > ${vcf_name}_all_var_table.txt 2>>data.ip

    mv ${dbsnp} ${vcf_name}_final.vcf.gz
    tabix ${vcf_name}_final.vcf.gz
    mv data.ip ${logname}
	"""
}
	// gzip -f ${vcf_name}_all_var_table.txt
// #	zcat ${dbsnp_af} \\
// #		| /app/snpEff/scripts/vcfEffOnePerLine.pl \\
// #		| java "-Xmx${avail_mem}M" -jar /app/snpEff/SnpSift.jar extractFields \\
// #		- CHROM ID POS REF ALT "ANN[*].GENE" GWASCAT_TRAIT GWASCAT_P_VALUE GWASCAT_OR_BETA \\
// #		> ${vcf_name}_all_gwas_table.txt
// #	gzip -f ${vcf_name}_all_gwas_table.txt            // path("*_all_gwas_table.txt.gz"),path("*_all_gwas_table.txt.gz.tbi"),
