# For meaning, see https://huggingface.co/spaces/evaluate-metric/chrf

import sys
from evaluate import load

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

    lines1 = read_lines(file1)
    lines2 = read_lines(file2)

    max_len = max(len(lines1), len(lines2))
    chrf = load("chrf")

    for i in range(max_len):
        line1 = lines1[i].rstrip('\n') if i < len(lines1) else ""
        line2 = lines2[i].rstrip('\n') if i < len(lines2) else ""
     
        predictions = [line2]
        references = [[line1]]

        # Calculate ChrF3
        results = chrf.compute(predictions=predictions, references=references, word_order=1, lowercase=True, beta=3)
        print(results)

if __name__ == "__main__":
    main()