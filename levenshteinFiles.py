import Levenshtein
from difflib import SequenceMatcher
import sys

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()

def main():
    file1 = sys.argv[1] # known-good (human-generated) file
    file2 = sys.argv[2] # AI-generated file

    text1 = read_file(file1)
    text2 = read_file(file2)

    distance = Levenshtein.distance(text1, text2)
    print(f"The Levenshtein distance between '{file1}' and '{file2}' is: {distance}")

    lines1 = read_lines(file1)
    lines2 = read_lines(file2)

    max_len = max(len(lines1), len(lines2))
    total_distance = 0
    total_chars = 0
    total_similarity_ratio = 0

    for i in range(max_len):
        line1 = lines1[i].rstrip('\n') if i < len(lines1) else ""
        line2 = lines2[i].rstrip('\n') if i < len(lines2) else ""
        distance = Levenshtein.distance(line1, line2)
        total_distance += distance
        total_chars += len(line2)
        #print(f"Line {i+1}: Levenshtein distance = {distance}", end="")

        matcher = SequenceMatcher(None, line1, line2)
        similarity_ratio = matcher.ratio() * 100
        total_similarity_ratio += similarity_ratio
        #print(f"\tSimilarity Ratio: {similarity_ratio:.1f}")

    print(f"Total sum of line-by-line Levenshtein distances: {total_distance} and average {(total_distance/max_len):.1f}")
    print(f"Length of file2 is {total_chars}, requiring a change of {(total_distance/total_chars*100):.1f}% of characters")
    print(f"Average line-based similarity {(total_similarity_ratio/max_len):.1f} out of 100")
    print("--------------------")

if __name__ == "__main__":
    main()