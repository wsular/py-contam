# Notes on Setting up contam-x-3.2 on aeolus

## Linux Executable
1. The linux executable, contam-x-3.2-gcc.exe, is installed on aeolus at /home/vonw/contamX.
2. The executable was downloaded from https://www.nist.gov/el/energy-and-environment-division-73200/nist-multizone-modeling/download-contam.

## Software
1. The software for running different simulations with contam-x were cloned at /home/vonw/work/software/iaq.
2. The command to clone the repository is:
   
   ```
   git clone https://github.com/wsular/py-contam.git
   ```
### removeFeb29_LeapYears

3. Removed leap years from all MACA files in /data/lar/users/vonw/iaq/data/maca.
4. I had to create an executable version of removeFeb29_LeapYears.py. 
5. I also had to create a qsub file for submitting the job on aeolus.
   
   ```
    #!/bin/bash
    #PBS -k o
    #PBS -l nodes=1:amd:ppn=1,walltime=00:30:00,mem=2gb
    #PBS -M v.walden@wsu.edu
    #PBS -m abe
    #PBS -N RemoveLeapYears
    #PBS -j oe
    #PBS -d /home/vonw/work/software/iaq/py-contam/python/maca
    /home/vonw/work/software/iaq/py-contam/python/maca/removeFeb29_LeapYears
   ```
6. This ran easily!!