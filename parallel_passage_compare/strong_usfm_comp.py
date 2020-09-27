import os
import xml.etree.ElementTree as ET

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
    book_arr.append(chapter_arr)
    return book_arr

def load_nt():
    #Returns new testament.
    #Access using obj["book"][chapter][verse]
    NT = {}
    NT["Matthew"] = load_strong_usfm(folder + "46-MATgrcmt.usfm")
    NT["Mark"] = load_strong_usfm(folder + "47-MRKgrcmt.usfm")
    NT["Luke"] = load_strong_usfm(folder + "48-LUKgrcmt.usfm")
    NT["John"] = load_strong_usfm(folder + "49-JHNgrcmt.usfm")
    NT["Acts"] = load_strong_usfm(folder + "50-ACTgrcmt.usfm")
    NT["Romans"] = load_strong_usfm(folder + "51-ROMgrcmt.usfm")
    NT["1 Corinthians"] = load_strong_usfm(folder + "52-1COgrcmt.usfm")
    NT["2 Corinthians"] = load_strong_usfm(folder + "53-2COgrcmt.usfm")
    NT["Galations"] = load_strong_usfm(folder + "54-GALgrcmt.usfm")
    NT["Ephesians"] = load_strong_usfm(folder + "55-EPHgrcmt.usfm")
    NT["Philippians"] = load_strong_usfm(folder + "56-PHPgrcmt.usfm")
    NT["Colossians"] = load_strong_usfm(folder + "57-COLgrcmt.usfm")
    NT["1 Thessalonians"] = load_strong_usfm(folder + "58-1THgrcmt.usfm")
    NT["2 Thessalonians"] = load_strong_usfm(folder + "59-2THgrcmt.usfm")
    NT["1 Timothy"] = load_strong_usfm(folder + "60-1TIgrcmt.usfm")
    NT["2 Timothy"] = load_strong_usfm(folder + "61-2TIgrcmt.usfm")
    NT["Titus"] = load_strong_usfm(folder + "62-TITgrcmt.usfm")
    NT["Philemon"] = load_strong_usfm(folder + "63-PHMgrcmt.usfm")
    NT["Hebrews"] = load_strong_usfm(folder + "64-HEBgrcmt.usfm")
    NT["James"] = load_strong_usfm(folder + "65-JASgrcmt.usfm")
    NT["1 Peter"] = load_strong_usfm(folder + "66-1PEgrcmt.usfm")
    NT["2 Peter"] = load_strong_usfm(folder + "67-2PEgrcmt.usfm")
    NT["1 John"] = load_strong_usfm(folder + "68-1JNgrcmt.usfm")
    NT["2 John"] = load_strong_usfm(folder + "69-2JNgrcmt.usfm")
    NT["3 John"] = load_strong_usfm(folder + "70-3JNgrcmt.usfm")
    NT["Jude"] = load_strong_usfm(folder + "71-JUDgrcmt.usfm")
    NT["Revelation"] = load_strong_usfm(folder + "72-REVgrcmt.usfm")
    return NT


def do_comparison(comp1,comp2):
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


def do_comparisons(verse1,comp1,verse2,comp2,verse3 = '',comp3=[],verse4 = '',comp4=[]):
    html = ''
    if(comp3==[]):
        results = [do_comparison(comp1,comp2),do_comparison(comp2,comp1)]
        html = '''  <tr>
    <th>{firstverse}</th>
    <th>{secondverse}</th>
  </tr>
  <tr>
    <td>{firstcomp}</td>
    <td>{secondcomp}</td>
  </tr>
'''.format(firstverse=verse1,secondverse=verse2,firstcomp=results[0],secondcomp=results[1])
    elif(comp4==[]):
        results =  [do_comparison(comp1,comp2+comp3),do_comparison(comp2,comp1+comp3),do_comparison(comp3,comp2+comp1)]
        html = '''  <tr>
    <th>{firstverse}</th>
    <th>{secondverse}</th>
    <th>{thirdverse}</th>
  </tr>
  <tr>
    <td>{firstcomp}</td>
    <td>{secondcomp}</td>
    <td>{thirdcomp}</td>
  </tr>
'''.format(firstverse=verse1,secondverse=verse2,thirdverse=verse3,firstcomp=results[0],secondcomp=results[1],thirdcomp=results[2])
    else:
        results =  [do_comparison(comp1,comp2+comp3+comp4),do_comparison(comp2,comp1+comp3+comp4),do_comparison(comp3,comp2+comp1+comp4),do_comparison(comp4,comp1+comp2+comp3)]
        html = '''  <tr>
    <th>{firstverse}</th>
    <th>{secondverse}</th>
    <th>{thirdverse}</th>
    <th>{fourthverse}</th>
  </tr>
  <tr>
    <td>{firstcomp}</td>
    <td>{secondcomp}</td>
    <td>{thirdcomp}</td>
    <td>{fourthcomp}</td>
  </tr>
'''.format(firstverse=verse1,secondverse=verse2,thirdverse=verse3,fourthverse=verse4,firstcomp=results[0],secondcomp=results[1],thirdcomp=results[2],fourthcomp=results[3])
    
    return html

###MAIN
folder = "D:\\Documents\\Strong_USFMs\\"
bible = load_nt()
all_parallels = ET.parse(folder + "nt-parallel-passages.xml")
root = all_parallels.getroot()
html = '''<html>
<table style="width:100%" border="1" width="200px" height="auto">
'''
for section in root:
    html = html + '''  <tr>
    <th>{sectionheader}</th>
  </tr>
'''.format(sectionheader=section.attrib["title"])
    print(section.attrib["title"])
    for _set in section:
        for reference in _set:
            if "-" in reference.attrib["verse"]:
                #print(reference.attrib["book"]+reference.attrib["chapter"])
                reference.attrib["comp"] = bible[reference.attrib["book"]][int(reference.attrib["chapter"])][int(reference.attrib["verse"].split("-")[0])]
                for i in range(int(reference.attrib["verse"].split("-")[0]),int(reference.attrib["verse"].split("-")[1])):
                    reference.attrib["comp"] = reference.attrib["comp"] + bible[reference.attrib["book"]][int(reference.attrib["chapter"])][i+1]
            else:
                #print("false")
                #print(reference.attrib["book"])
                reference.attrib["comp"] = bible[reference.attrib["book"]][int(reference.attrib["chapter"])][int(reference.attrib["verse"])]
            reference.attrib["print_name"] = reference.attrib["book"] + " " + reference.attrib["chapter"] + ":" + reference.attrib["verse"]
        if len(_set) == 4:
            html = html + do_comparisons(_set[0].attrib["print_name"],_set[0].attrib["comp"],_set[1].attrib["print_name"],_set[1].attrib["comp"],_set[2].attrib["print_name"],_set[2].attrib["comp"],_set[3].attrib["print_name"],_set[3].attrib["comp"])
        elif len(_set) == 3:
            html = html + do_comparisons(_set[0].attrib["print_name"],_set[0].attrib["comp"],_set[1].attrib["print_name"],_set[1].attrib["comp"],_set[2].attrib["print_name"],_set[2].attrib["comp"])
        elif len(_set) == 2:
            html = html + do_comparisons(_set[0].attrib["print_name"],_set[0].attrib["comp"],_set[1].attrib["print_name"],_set[1].attrib["comp"])


html = html + '''</table>
</html>'''
            
with open(folder + 'out.html', 'w', encoding="utf-8") as f:
    f.write(html)
