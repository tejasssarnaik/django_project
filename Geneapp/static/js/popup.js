document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        var fastq1 = document.getElementsByName('fastq1')[0];
        var fastq2 = document.getElementsByName('fastq2')[0];

        if (!fastq1.files.length || !fastq2.files.length) {
            alert('Please select both FastQ1 and FastQ2 files.');
            event.preventDefault(); // Prevent the form from submitting
        }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('uploadForm').addEventListener('submit', function(event) {
//         var workflowOption = document.querySelector('input[name="workflow_option"]:checked');
//         var workflowName = document.getElementById('workflowName');
//         var fastq1 = document.getElementsByName('fastq1')[0];
//         var fastq2 = document.getElementsByName('fastq2')[0];
//         var referenceGenome = document.querySelector('input[name="reference_genome"]:checked');

//         // Check if FastQ1 and FastQ2 files are selected
      

//         // Check if workflow option is selected
//         if (!workflowOption) {
//             alert('Please select a workflow option.');
//             event.preventDefault();
//             return;
//         }

//         // Check if workflow name is entered
//         if (workflowName.value.trim() === '') {
//             alert('Please enter a workflow name.');
//             event.preventDefault();
//             return;
//         }
//             // Check if FastQ1 and FastQ2 files are selected
//         if (!fastq1.files.length || !fastq2.files.length) {
//             alert('Please select both FastQ1 and FastQ2 files.');
//             event.preventDefault(); // Prevent the form from submitting
//             return;
//         }

//         // Check if reference genome is selected
//         if (!referenceGenome) {
//             alert('Please select a reference genome.');
//             event.preventDefault();
//             return;
//         }
//     });
// });


