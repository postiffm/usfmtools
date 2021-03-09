#!/usr/bin/python3
#import xml
import xml.etree.ElementTree as ET
from xml.dom import minidom

# See https://pymotw.com/2/xml/etree/ElementTree/create.html
# and https://docs.python.org/3/library/xml.etree.elementtree.html

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

print("Reading XML")

tree = ET.parse('Example Term.xml')
root = tree.getroot()

print("Root = ", root.tag)
print("Root Attribute = ", root.attrib)
for child in root:
    print(child.tag, child.attrib)

ET.dump(root)

print("Writing new XML")

# Make a new tree, then fill it
tree = ET.ElementTree()
a = ET.Element('a')
#tree = ET.ElementTree(a)
tree._setroot(a)
b = ET.SubElement(a, 'b')
c = ET.SubElement(a, 'c')
d = ET.SubElement(c, 'd')

# Write to STDOUT, then to file
ET.dump(tree) # ET.dump(a) also works
tree.write('output.xml')
print(prettify(a)) # I don't understand why I cannot pass "tree" instead of "a"
