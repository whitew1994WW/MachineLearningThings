import re
import HTMLParser

def find_reg(regex, text):
    matches = re.finditer(regex, text, re.MULTILINE)
    groups = [match.group(1) for match in matches]
    return groups

test_string = "\"calories\">345<hdfghdfg"
regexp = r'\"calories\">(\d*)<'

#assert find_reg(regexp, test_string) == ['345']

# testing the find and replace part of python strings

test_str = "&amp;"
test_str = HTMLParser.HTMLParser().unescape(test_str)
test_str.replace("&", "and")
print(test_str)
#assert test_str == "and"