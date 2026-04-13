import os
import subprocess
import sys

# Wrapper to run levenshteinFiles.py, which now does way more than just the levenshtein algorithm.

# How to Set up environment
# First time:
# python3 -m venv .ubuvenv or .wslvenv or .deskvenv (henceforth I will call this .venv)
# I mention different names because of cross-platform problems. You cannot use your ubuntu
# env with wsl if you are in a shared folder provided by (say) Dropbox
# pip3 install -r evalRequirements.txt
# The important components of this are evaluate sacrebleu Levenshtein

# Every time you log in:
# source .venv/bin/activate

# Usage:
# Update the files list in files.py in the current working directory with the files you want to process
# python3 evalAIDraft.py

# Shorthand for some scripts - I need to make this path independent 
USFMTOOLS = "../../AndroidApps/usfmtools"
USFMtoACC = f"{USFMTOOLS}/usfmToAccordance.py"
LEV = f"{USFMTOOLS}/levenshteinFiles.py"

# Add the current working directory to the module search path
sys.path.insert(0, os.getcwd())
# This allows the import below from the current directory to work
# List of tuples - (good file SFM, AI-draft SFM)... file from lrl-engine
from files import files

folder = sys.argv[1] if len(sys.argv) > 1 else "."

#for filename in os.listdir(folder):
#    if filename.endswith(".usfm"):
#        filepath = os.path.join(folder, filename)
#        subprocess.run(["bash", "run.sh", filepath])

# Walk through all Bible books in files. Simplify the USFM
# to the Accordance format that we have been using as a basis
# of comparison. Then run the levenshteinFiles.py script, which
# is a bit misnamed because it also does a chrF3 calculation
# as well as the difflib SequenceMatcher comparison.

for goodF, aiF in files:
    goodAcc = goodF.replace("SFM", "acc")
    aiAcc = aiF.replace("SFM", "acc")
    with open(goodAcc, 'w') as f:
        subprocess.run(["python3", USFMtoACC, "--no-para", goodF], stdout=f)   # good SFM > acc
    with open(aiAcc, 'w') as f:
        subprocess.run(["python3", USFMtoACC, "--no-para", aiF], stdout=f)     # ai SFM > acc
    subprocess.run(["python3", LEV, goodAcc, aiAcc])
