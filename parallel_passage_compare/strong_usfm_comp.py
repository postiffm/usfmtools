import os

def load_strong_usfm(filename):
    #returns compound array where first index is chapter,
    #second index is verse, and then [0] is word [1] strong id
    book = open(filename,encoding="utf8")
    lines = book.readlines()
    book_arr = []
    chapter_arr = []
    for line in lines:
        if line[1] == "c":
            #print("chapter")
            book_arr.append(chapter_arr)
            chapter_arr = []
            #offset since no verse 0
            chapter_arr.append([])
        elif line[1] == "v":
            #print("verse")
            words = line.split("\\w")
            verse = []
            #TODO say how this works
            for word in words:
                if "strong" in word:
                    text_word = word.split(" ")[1]
                    strong = word.split('"')[1]
                    verse.append([text_word,strong])
            chapter_arr.append(verse)
            
    return book_arr

def load_nt():
    #Returns new testament.
    #Access using obj["book"][chapter][verse]
    NT = {}
    NT["MAT"] = load_strong_usfm(folder + "46-MATgrcmt.usfm")
    NT["MRK"] = load_strong_usfm(folder + "47-MRKgrcmt.usfm")
    NT["LUK"] = load_strong_usfm(folder + "48-LUKgrcmt.usfm")
    NT["JHN"] = load_strong_usfm(folder + "49-JHNgrcmt.usfm")
    NT["ACT"] = load_strong_usfm(folder + "50-ACTgrcmt.usfm")
    NT["ROM"] = load_strong_usfm(folder + "51-ROMgrcmt.usfm")
    NT["1CO"] = load_strong_usfm(folder + "52-1COgrcmt.usfm")
    NT["2CO"] = load_strong_usfm(folder + "53-2COgrcmt.usfm")
    NT["GAL"] = load_strong_usfm(folder + "54-GALgrcmt.usfm")
    NT["EPH"] = load_strong_usfm(folder + "55-EPHgrcmt.usfm")
    NT["PHP"] = load_strong_usfm(folder + "56-PHPgrcmt.usfm")
    NT["COL"] = load_strong_usfm(folder + "57-COLgrcmt.usfm")
    NT["1TH"] = load_strong_usfm(folder + "58-1THgrcmt.usfm")
    NT["2TH"] = load_strong_usfm(folder + "59-2THgrcmt.usfm")
    NT["1TI"] = load_strong_usfm(folder + "60-1TIgrcmt.usfm")
    NT["2TI"] = load_strong_usfm(folder + "61-2TIgrcmt.usfm")
    NT["TIT"] = load_strong_usfm(folder + "62-TITgrcmt.usfm")
    NT["PHM"] = load_strong_usfm(folder + "63-PHMgrcmt.usfm")
    NT["HEB"] = load_strong_usfm(folder + "64-HEBgrcmt.usfm")
    NT["JAS"] = load_strong_usfm(folder + "65-JASgrcmt.usfm")
    NT["1PE"] = load_strong_usfm(folder + "66-1PEgrcmt.usfm")
    NT["2PE"] = load_strong_usfm(folder + "67-2PEgrcmt.usfm")
    NT["1JN"] = load_strong_usfm(folder + "68-1JNgrcmt.usfm")
    NT["2JN"] = load_strong_usfm(folder + "69-2JNgrcmt.usfm")
    NT["3JN"] = load_strong_usfm(folder + "70-3JNgrcmt.usfm")
    NT["JUD"] = load_strong_usfm(folder + "71-JUDgrcmt.usfm")
    NT["REV"] = load_strong_usfm(folder + "72-REVgrcmt.usfm")
    return NT


def do_comparison(bible,comp1,comp2):
    comp_result = ""
    
    exact_open = '<span style="background-color:green">'
    exact_close = "</span>"
    root_open = '<span style="background-color:yellow">'
    root_close = "</span>"
    sorta_open = '<span style="background-color:orange">'
    sorta_close = "</span>"
    
    for word in comp1:
        sorta_match = False
        exact_match = False
        root_match = False
        for compword in comp2:
            if compword[1] == word[1]:
                root_match = True
                if compword[0] == word[0]:
                    exact_match = True
                    break
            elif word[0][0:4] in compword[0]:
                sorta_match = True
        if exact_match:
            comp_result = comp_result + exact_open
        elif root_match:
            comp_result = comp_result + root_open
        elif sorta_match:
            comp_result = comp_result + sorta_open
        comp_result = comp_result + word[0]
        if exact_match:
            comp_result = comp_result + exact_close
        elif root_match:
            comp_result = comp_result + root_close
        elif sorta_match:
            comp_result = comp_result + sorta_close
        comp_result = comp_result + " "
    return comp_result


def do_comparisons(bible,verse1,comp1,verse2,comp2,verse3 = '',comp3=[]):
    html = ''
    if(comp3==[]):
        results = [do_comparison(bible,comp1,comp2),do_comparison(bible,comp2,comp1)]
        html = '''<table style="width:100%" border="1" width="200px" height="auto">
  <tr>
    <th>{firstverse}</th>
    <th>{secondverse}</th>
  </tr>
  <tr>
    <td>{firstcomp}</td>
    <td>{secondcomp}</td>
  </tr>
</table>'''.format(firstverse=verse1,secondverse=verse2,firstcomp=results[0],secondcomp=results[1])
    else:
        results =  [do_comparison(bible,comp1,comp2+comp3),do_comparison(bible,comp2,comp1+comp3),do_comparison(bible,comp3,comp2+comp1)]
        html = '''<table style="width:100%" border="1" width="200px" height="auto">
  <tr>
    <th>{firstverse}</th>
    <th>{secondverse}</th>
    <th>{thirdverse}</th>
  </tr>
  <tr>
    <td>{firstcomp}</td>
    <td>{secondcomp}</td>
    <td>{thirdcomp}</td>
  </tr>
</table>'''.format(firstverse=verse1,secondverse=verse2,thirdverse=verse3,firstcomp=results[0],secondcomp=results[1],thirdcomp=results[2])
    return html


folder = "D:\\Documents\\Strong_USFMs\\"
bible = load_nt()
comp1 = bible["MAT"][3][1]+bible["MAT"][3][2]
comp2 = bible["MRK"][1][4]
comp3 = bible["LUK"][3][3]
html_result = do_comparisons(bible,"Matthew 3:1-2",comp1,"Mark 1:4",comp2,"Luke 3:3",comp3)

with open(folder + 'out.html', 'w', encoding="utf-8") as f:
    f.write(html_result)
