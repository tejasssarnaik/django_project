process ACTIONABLES{
    tag "${sampleid}"
    label 'process_medium'
    queue 'medium'

    container 'glslabs/bcftools:latest'

    input:
    tuple val(sampleid), val(vcf_name), path(table1), path(header)
    path (logf), stageAs: 'data.ip'
    val  (logname)

    output:
    tuple val(sampleid), path("*variants*"), emit: table, optional: true
    path ("*"), optional: true
    path "*.log" , emit: loge

    when:
    task.ext.when == null || task.ext.when

    script:
    """
    echo ">> CLINICAL-SIG-ACTIONABLES - LOG FILE" >>data.ip
    function SIG () {
    # Actionable variants separation
    cat "${table1}" | grep -E "Pathogenic|Likely_pathogenic" > ${sampleid}_variants_pathogenic.txt
    cat ${header} ${sampleid}_variants_pathogenic.txt > ${sampleid}_newfile.txt
    mv ${sampleid}_newfile.txt ${sampleid}_variants_pathogenic.txt

    #all pathogenic
    cat "${table1}" | grep -E "Pathogenic|Likely_pathogenic" > ${sampleid}_variants_pathogenic.txt
    cat ${header} ${sampleid}_variants_pathogenic.txt > ${sampleid}_newfile
    mv ${sampleid}_newfile ${sampleid}_variants_pathogenic.txt

    #all risk factor
    cat "${table1}" | grep "risk_factor" > ${sampleid}_variants_riskfactor.txt
    cat ${header} ${sampleid}_variants_riskfactor.txt > ${sampleid}_newfile
    mv ${sampleid}_newfile ${sampleid}_variants_riskfactor.txt

    #all protective
    cat "${table1}" | grep "protective" > ${sampleid}_variants_protective.txt
    cat ${header} ${sampleid}_variants_protective.txt > ${sampleid}_newfile
    mv ${sampleid}_newfile ${sampleid}_variants_protective.txt

    #all drug response
    cat "${table1}" | grep "drug_response" > ${sampleid}_variants_drug_response.txt
    cat ${header} ${sampleid}_variants_drug_response.txt > ${sampleid}_newfile
    mv ${sampleid}_newfile ${sampleid}_variants_drug_response.txt
    }

    SIG 2>>data.ip
    mv data.ip ${logname}
    """
}
    // #file2=\$(basename "${table2}" | sed -E 's/\\.gz\$//')
    // #unzip ${table2}
    // #tbljoin -lr -n 1 "\${file1}" "\${file2}" > "${sampleid}_all_actionable_variants.txt"
    // filter=("risk_factor" "protective" "drug_response")
    // for f in "\${filter[@]}";
    // do
    //     ACT_FILTER_TABLE "${sampleid}_all_actionable_variants.txt" "\$f" 
    // done
    // function ACT_FILTER_TABLE () {
    //     cat \$1 | grep -E \$2 > ${sampleid}_variants_\$2.txt
    //     cat ${header} ${sampleid}_variants_\$2.txt > ${sampleid}_newfile.txt
    //     mv ${sampleid}_newfile.txt ${sampleid}_variants_\$2.txt

    //     return ${sampleid}_variants_\$2.txt
    // }
