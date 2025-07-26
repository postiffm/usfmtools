import Levenshtein
from difflib import SequenceMatcher

# TheLevenshtein algorithm measures the minimum number of single-character edits 
# (insertions, deletions, or substitutions) required to change one text into
# another. s1 is the known-good string in my case, and s2 is the AI-generated
# variant.

def main():
    #s1 = input("Enter the first string: ")
    #s2 = input("Enter the second string: ")
    s1 = "Cuih cān ah, baptisma petu John cu a feh ih, Judia peng ramṭhing ah thu a sim. Nan lungthleng uh, ziangahtile vancung uknak cu a nai zo, tiah a ti."
    s2 = "Cu laiah baptisma petu John a ra ih, Judia peng ramṭhing ah thu a sim. Nan lungthleng uh, ziangahtile van uknak cu a nai zo! tiah a ti."
    s1Len = len(s1)
    s2Len = len(s2)
    distance = Levenshtein.distance(s1, s2)
    print(f"The Levenshtein distance between s1 and s2 is: {distance}")
    print(f"Length of s2 is {s2Len}, requiring a change of {(distance/s2Len*100):.1f}% of characters")

    matcher = SequenceMatcher(None, s1, s2)
    similarity_ratio = matcher.ratio()
    print(f"Similarity Ratio: {similarity_ratio*100:.1f}")

if __name__ == "__main__":
    main()
    