from HTMLParser import HTMLParser

#For stripping html formatting from the text
class HTMLParser2(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = HTMLParser2()
    s.feed(html)
    return s.get_data()