#!/bin/python3
import subprocess
import time
import os


def RUN_FASTQC (config_file,fastqc_path):
    gafastqc = os.path.abspath(fastqc_path)
    full_path = os.path.abspath(config_file)
    # command to be executed
    print("RUNNING GENEASSURE FASTQC")
    command = f"bash {gafastqc} -c {full_path} run"

    # Run the command using subprocess
    process = subprocess.Popen(command, shell=True)

    # Display running status until the process finishes
    while process.poll() is None:
        print("Process is still running...")
        time.sleep(5)  # Adjust the sleep duration as needed

    # Process has ended
    print("Process ended!")


# Usage:
# config_file = "./configs"
# gafastqc_path='./gafastqc'
# RUN_FASTQC(config_file,gafastqc_path)