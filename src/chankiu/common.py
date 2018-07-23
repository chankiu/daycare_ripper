from html.parser import HTMLParser
import unicodedata

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def remove_lines_tabs(input):
    output = input.replace('\n', '')
    output = input.replace('\t', '')
    return output


def clean_string(input):
    # Remove HTML Tags
    output = strip_tags(input)

    # Remove Unicode characters
    output = unicodedata.normalize('NFKD', output).encode('ascii','ignore').decode('ascii')

    # Remove lines and tabs
    output = remove_lines_tabs(output)
    return output