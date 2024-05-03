process BAM_HTMLS {

    input:

    output:

    script:
    """
    python $baseDir/bin/bamQC.py
    python $baseDir/bin/plots_bamQC.py
    """
}