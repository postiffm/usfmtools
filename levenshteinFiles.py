import Levenshtein
from difflib import SequenceMatcher
import sys
from evaluate import load
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Just do this the first time
#nltk.download('punkt_tab')

# Levenshtein
# Python similarity metric
# chrF3 For meaning, see https://huggingface.co/spaces/evaluate-metric/chrf
# BLEU score 
# (C) Matt Postiff, 2026

# Python environment setup
# python3 -m venv .env
# .env/bin/pip install Levenshtein
# .env/bin/pip install evaluate
# .env/bin/pip install sacrebleu
# You can also source .env/bin/activate (and deactivate when done) so don't have to type .env/bin/ all the time.
# This /should/ be taken care of by the evalAIDraft.py wrapper script

# Usage: python3 levenshteinFiles.py goldStandard AIDraft
# Assumes the files are in .acc format from usfmToAccordance

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
def read_verses(filename):
    verses = dict()  # Map from verse address to text so that we can line up verses between goldStandard and AIDraft
    with open(filename, "r", encoding="utf-8") as f:
        #return f.readlines()
        for ln in f.readlines():
            # Each line is in the format Book. c:v text and I want to index a dictionary based on "book. c:v"
            m = re.match(r'^(.+?\s+\d+:\d+\s*)(.*)$', ln)
            if m:
                addr = m.group(1)
                text = m.group(2)
                verses[addr] = text
            else:
                print(f"Did not handle verse=>{ln}")
    return verses

def straighten_quotes(text):
    text = text.replace('“', '"')  # Left double smart quote
    text = text.replace('”', '"')  # Right double smart quote
    text = text.replace('‘', "'")  # Left single smart quote
    text = text.replace('’', "'")  # Right single smart quote
    text = text.replace('”', '"')  # Typo in a source snippet
    text = text.replace('“', '"')  # Typo in a source snippet
    return text

def main():
    file1 = sys.argv[1] # known-good (human-generated) file
    file2 = sys.argv[2] # AI-generated file

    text1 = read_file(file1)
    text2 = read_file(file2)

    distance = Levenshtein.distance(text1, text2)
    print(f"{file1} and {file2} Levenshtein distance is: {distance}")

    verses1 = read_verses(file1)
    verses2 = read_verses(file2)

    chrf = load("chrf")
    total_distance = 0
    total_chars = 0
    total_similarity_ratio = 0
    versesNotFound = 0
    totalVersesCompared = 0
    chrF3TotalScore = 0
    total_bleu = 0

    for addr in verses1:
        if (addr not in verses2):  
            #print(f"{addr} not found in AI candidate")
            versesNotFound += 1
            continue
        # From here, we know the verse address is in both dictionaries
        line1 = verses1[addr].rstrip('\n')
        line2 = verses2[addr].rstrip('\n')
        # Standardizing everything to lowercase makes about 0.2 difference
        line1 = line1.lower()
        line2 = line2.lower()
        # Matching quote-style makes a similar additional difference
        line1 = straighten_quotes(line1)
        line2 = straighten_quotes(line2)
        #print(f"Comparing {line1}    to\n          {line2}")

        # Levensthein algorithm
        distance = Levenshtein.distance(line1, line2)
        total_distance += distance
        total_chars += len(line2)
        #print(f"Line {i+1}: Levenshtein distance = {distance}", end="")

        # chrF3 n-gram algorithm
        prediction = [line2]
        reference = [[line1]]
        # I had wordorder at 1 for all my stuff.
        results = chrf.compute(predictions=prediction, references=reference, word_order=0, lowercase=True, beta=3)
        #print(f"reference_text: {reference}")
        #print(f"predicted_text: {prediction}")
        lineScore = results["score"]
        #print(f"chrf: {lineScore}")
        totalVersesCompared += 1
        chrF3TotalScore += lineScore

        # Bleu Score
        prediction = word_tokenize(line2)
        reference = [word_tokenize(line1)]
        score = sentence_bleu(reference, prediction, smoothing_function=SmoothingFunction().method1)
        total_bleu += score
        #print(f"score={score} {type(score)} Bleu={(score):.6e} total_bleu={(total_bleu):0.6e}")

        # Python's difflib "similarity" algorithm. It uses a modified version of the Ratcliff and Obershelp "gestalt 
        # pattern matching" algorithm. It works by recursively finding the longest contiguous matching subsequences 
        # that contain no "junk" elements.
        matcher = SequenceMatcher(None, line1, line2)
        similarity_ratio = matcher.ratio() * 100
        total_similarity_ratio += similarity_ratio
        #print(f"\tSimilarity Ratio: {similarity_ratio:.1f}")

    totalVerses = len(verses1)
    pctCharsToChange = (total_distance/total_chars*100)
    print(f"    {versesNotFound} verses are not present in the AI candidate out of total of {totalVerses} verses and {totalVersesCompared} lines")
    print(f"    Sum of line-by-line Levenshtein distances: {total_distance} and average {(total_distance/totalVerses):.1f}")
    print(f"    Length of file2 is {total_chars}, requiring a change of {pctCharsToChange:.1f}% of characters or Lev similarity = {(100-pctCharsToChange):.1f}%")
    print(f"    chrF3 total score = {chrF3TotalScore:.1f} and average = {(chrF3TotalScore/totalVersesCompared):.1f}")
    print(f"    Average BLEU Score: {(total_bleu/totalVerses):.4f}") # Output: ~1.0000 for perfect match
    print(f"    Average line-based similarity {(total_similarity_ratio/totalVerses):.1f} out of 100")
    print("--------------------")

if __name__ == "__main__":
    main()
