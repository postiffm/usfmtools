import os
import subprocess
import sys

# Usage:
# Update the files list below with the files you want to process
# python3 evalAIDraft.py

# Shorthand for some scripts
USFMTOOLS = "../../AndroidApps/usfmtools"
USFMtoACC = f"{USFMTOOLS}/usfmToAccordance.py"
LEV = f"{USFMTOOLS}/levenshteinFiles.py"

# List of tuples - good file, AI-draft file from lrl-engine
files = [
("08RUTCSV.SFM", "rut_bsb_falam_04042026.usfm"),
("32JONCSV.SFM", "jon_bsb_falam_04052026.usfm"),
]

folder = sys.argv[1] if len(sys.argv) > 1 else "."

#for filename in os.listdir(folder):
#    if filename.endswith(".usfm"):
#        filepath = os.path.join(folder, filename)
#        subprocess.run(["bash", "run.sh", filepath])

# Walk through all Bible books in files. Simplify the USFM
# to the Accordance format that we have been using as a basis
# of comparison. Then run the levenshteinFiles.py script, which
# is a bit misnamed because it also doesa  chrF3 calculation
# as well as 

for goodF, aiF in files:
    goodAcc = goodF.replace("SFM", "acc")
    aiAcc = aiF.replace("usfm", "acc")
    with open(goodAcc, 'w') as f:
        subprocess.run(["python3", USFMtoACC, "--no-para", goodF], stdout=f)   # good SFM > acc
    with open(aiAcc, 'w') as f:
        subprocess.run(["python3", USFMtoACC, "--no-para", aiF], stdout=f)     # ai usfm > acc
    subprocess.run(["python3", LEV, goodAcc, aiAcc])

