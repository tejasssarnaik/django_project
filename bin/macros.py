from vcfstats.macros import categorical
from vcfstats.macros import continuous
from vcfstats.macros import aggregation

@categorical
def VARTYPE(variant):
  """Variant type, one of deletion, indel, snp or sv"""
  return variant.var_type

@categorical
def TITV(variant):
  """Tell if a variant is a transition or transversion. The variant has to be an snp first."""
  if not variant.is_snp:
	  return False
  return 'transition' if variant.is_transition else 'transversion'

@categorical(alias = 'CHROM')
def CONTIG(variant):
  """Get the config/chromosome of a variant. Alias: CHROM"""
  return variant.CHROM

@categorical(alias = 'GT_TYPEs')
def GTTYPEs(variant):
  """Get the genotypes(HOM_REF,HET,HOM_ALT,UNKNOWN) of a variant for each sample"""
  gttypes = variant.gt_types
  return ['HOM_REF'if gttype == 0 else \
		  'HET' if gttype == 1 else \
		  'HOM_ALT' if gttype == 2 else 'UNKNOWN' for gttype in gttypes]

@categorical
def FILTER(variant):
  """Get the FILTER of a variant."""
  return variant.FILTER or 'PASS'

@categorical
def SUBST(variant):
  """Substitution of the variant, including all types of varinat"""
  return '{}>{}'.format(variant.REF, ','.join(variant.ALT))

@categorical
def Allelic_Type(variant):
    """Get allelic type, either biallelic or multiallelic"""
    return "biallelic" if len(variant.ALT) == 1 else "multi-allelic"


@categorical
def N_Allelic(variant):
    """Get number of alleles"""
    return len(variant.ALT) + 1

@continuous
def NALT(variant):
  """Number of alternative alleles"""
  return len(variant.ALT)

@continuous
def GQs(variant):
  """get the GQ for each sample as a numpy array."""
  return variant.gt_quals

@continuous
def QUAL(variant):
  """Variant quality from QUAL field."""
  return variant.QUAL

@continuous(alias = 'DPs')
def DEPTHs(variant):
  """Get the read-depth for each sample as a numpy array."""
  return [sum(dp) for dp in variant.format('DP')]

@continuous
def AAF(variant):
  """Alternate allele frequency across samples in this VCF."""
  return variant.aaf

@continuous
def AFs(variant):
  """get the freq of alternate reads as a numpy array."""
  return variant.gt_alt_freqs

@continuous
def _ONE(variant):
  """Return 1 for a variant, usually used in aggregation, or indication of a distribution plot"""
  return 1

@continuous
def INFO_DP(variant):
    """DP from INFO"""
    return variant.INFO["DP"]


@continuous
def MISSINGs(variant):
    """DP from INFO"""
    # convert boolean array to int
    # gts012 = True
    return (variant.gt_types == 3) + 0


@continuous
def N_MISSING(variant):
    """DP from INFO"""
    # convert boolean array to int
    # gts012 = True
    return variant.num_unknown

@continuous
def Percent_HETs(variant):
    """Get % of HETs per locus"""
    return variant.num_het / float(len(variant.gt_types))

@aggregation
def COUNT(entries):
  """Count the variants in groups"""
  return len(entries)

@aggregation
def SUM(entries):
  """Sum up the values in groups"""
  return sum(entries)

@aggregation(alias = 'AVG')
def MEAN(entries):
  """Get the mean of the values"""
  if not entries:
	  return 0.0
  return sum(entries) / len(entries)
