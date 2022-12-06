import re
string="a==b && c==d || e==f"

# regex that matches all the conditions and the operators between them (&& and ||) apart from the last one
regex = re.compile(r"((\w+==\w+)(\s*(\|\||&&)\s*)?)+")
# find all the conditions
conditions = regex.findall(string)
print(conditions)