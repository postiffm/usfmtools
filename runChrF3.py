from evaluate import load

chrf = load("chrf")
predictions = ["The cat sat on the mat.", "The dog barked loudly."]
references = [["The cat sat on the mat."    ], ["The dog barked."]]

# Calculate ChrF3
results = chrf.compute(predictions=predictions, references=references, beta=3)
print(results)
