workflow VCF_STATISTICS{
	take:
	vcf

	main:
	BCFTOOLS_STATISTICS(vcf)
	stats1 = BCFTOOLS_STATISTICS.out.stats
	VCFSTATS(vcf)
	stats2 = VCFSTATS.out.stats

	emit:
	stats1
	stats2
}