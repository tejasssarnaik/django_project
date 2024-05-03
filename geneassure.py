#!/bin/usr/python3
# import subprocess
# import os
# import time
# import platform


# def run_nextflow(main_nf='main.nf', params_file='test.json', profile='awsbatch', process='WES'):

#     os_name = platform.system()

#     if os_name == "Linux":

#         # Check for Nextflow command
#         nextflow_check = subprocess.run("nextflow -v", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if nextflow_check.returncode == 0:
#             print("Nextflow is installed in linux")
#         else:
#             print("Nextflow is not installed in linux")
#             exit

#         # Check for AWS CLI command
#         aws_check = subprocess.run("aws --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if aws_check.returncode == 0:
#             print("AWS CLI is installed in linux")
#         else:
#             print("AWS CLI is not installed in linux")
#             exit

#         # Check for Docker command
#         docker_check = subprocess.run("docker --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if docker_check.returncode == 0:
#             print("Docker is installed")
#         else:
#             print("Docker is not installed in linux")
#             exit

# # command to be executed
#         print("RUNNING GENEASSURE IN LINUX SYSTEM")
#         command = f"nextflow run {main_nf} -params-file {params_file} -profile {profile}"

#     elif os_name == "Windows":

#         # Check for Docker command
#         docker_check = subprocess.run("docker --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if docker_check.returncode == 0:
#             print("Docker is not installed in windows")
#         else:
#             print("Docker is not installed in windows")
#             exit
# # command to be executed
#         print("RUNNING GENEASSURE IN WINDOWS SYSTEM")
#         command = f"docker run -v {os.getcwd()}:/pwd nextflow/nextflow:latest nextflow run /pwd/{main_nf} -params-file /pwd/{params_file} -profile 'awsbatch' --sequencing_type {process} --csv /pwd/GeneAssure/metadata.csv"
#     else:
#         print(f"error: system OS is not recognizable")
#         exit



#     # Run the command using subprocess
#     process = subprocess.Popen(command, shell=True)

#     # Display running status until the process finishes
#     while process.poll() is None:
#         print("Process is still running...")
#         time.sleep(5)  # Adjust the sleep duration as needed

#     # Process has ended
#     print("Process ended!")



# # Usage:
# run_nextflow(params_file='data.json',profile="awsbatch")


#!/bin/usr/python3
import subprocess
import os
import time
import platform


def run_nextflow(main_nf='main.nf', params_file='test.json', profile='awsbatch', process='WES'):

  
    command = f"docker run -v {os.getcwd()}:/pwd nextflow/nextflow:latest nextflow run /pwd/{main_nf} -params-file /pwd/{params_file} -profile 'awsbatch' --sequencing_type {process} --csv /pwd/GeneAssure/metadata.csv"
    

        # Run the command using subprocess
    process = subprocess.Popen(command, shell=True)

        # Display running status until the process finishes
    while process.poll() is None:
            print("Process is still running...")
            time.sleep(5)  # Adjust the sleep duration as needed

        # Process has ended
    print("Process ended!")



# Usage:
run_nextflow(params_file='data.json',profile="awsbatch")