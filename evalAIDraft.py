import os
import subprocess
import sys

 # How to Set up environment
# First time:
# python3 -m venv .ubuvenv or .wslvenv or .deskvenv
# pip3 install -r evalRequirements.txt
# On Ubuntu:
# source .ubuvenv/bin/activate
# On Windows Laptop:
# source .wslvenv/bin/activate
# pip3 install evaluate sacrebleu levenshtein
# Thereafter, just do the source command appropriate for the platform.

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
    ("01GENCSV.SFM", ""),
    ("02EXOCSV.SFM", ""),
    ("03LEVCSV.SFM", ""),
    ("04NUMCSV.SFM", ""),
    ("05DEUCSV.SFM", ""),
    ("06JOSCSV.SFM", ""),
    ("07JDGCSV.SFM", ""),
    ("08RUTCSV.SFM", ""),
    ("091SACSV.SFM", ""),
    ("102SACSV.SFM", ""),
    ("111KICSV.SFM", ""),
    ("122KICSV.SFM", ""),
    ("131CHCSV.SFM", ""),
    ("142CHCSV.SFM", ""),
    ("15EZRCSV.SFM", ""),
    ("16NEHCSV.SFM", ""),
    ("17ESTCSV.SFM", ""),
    ("18JOBCSV.SFM", ""),
    ("19PSACSV.SFM", ""),
    ("20PROCSV.SFM", ""),
    ("21ECCCSV.SFM", ""),
    ("22SNGCSV.SFM", ""),
    ("23ISACSV.SFM", ""),
    ("24JERCSV.SFM", ""),
    ("25LAMCSV.SFM", ""),
    ("26EZKCSV.SFM", ""),
    ("27DANCSV.SFM", ""),
    ("28HOSCSV.SFM", ""),
    ("29JOLCSV.SFM", ""),
    ("30AMOCSV.SFM", ""),
    ("31OBACSV.SFM", ""),
    ("32JONCSV.SFM", ""),
    ("33MICCSV.SFM", ""),
    ("34NAMCSV.SFM", ""),
    ("35HABCSV.SFM", ""),
    ("36ZEPCSV.SFM", ""),
    ("37HAGCSV.SFM", ""),
    ("38ZECCSV.SFM", ""),
    ("39MALCSV.SFM", ""),
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
