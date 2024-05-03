process fasta_index {

output:
path("*.txt") , emit: fasta_index

ref_genome = file( params.fasta, checkIfExists: true )
ref_dir    = ref_genome.getParent()
ref_name   = ref_genome.getBaseName()
ref_dict   = file( "${ref_dir}/${ref_name}.dict", checkIfExists: true )
ref_index  = file( "${ref_dir}/${ref_name}.{fasta|fna|fa}.fai", checkIfExists: true )

Channel
    .of(ref_genome,ref_dict ,ref_index)
    .collectFile(name: 'sample.txt', newLine: true)
    .subscribe {
        println "Entries are saved to file: $it"
        println "File content is: ${it.text}"
    }

}

