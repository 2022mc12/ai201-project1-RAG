from html.parser import HTMLParser

class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.capture = False
        self.buffer = [] # to deal with fragmented paragraphs
        
    def handle_starttag(self, tag, attrs):
        if tag in ("p", "li", "h5"):
            self.capture = True
            self.buffer = []

    def handle_endtag(self, tag):
        if tag in ("p", "li", "h5"):
            self.capture = False

            line = "".join(self.buffer).strip()
            if line:
                self.text.append(line)

    def handle_data(self, data):
        if self.capture:
            clean = data.strip()
            if clean:
                self.buffer.append(clean + " ")


file_titles = ["Commuting Effects on College Experience", "Off Campus Housing", "Transportation Experience", "NYU Neighborhood Resource Page", "NYU Commuter Resource Page"]
file_sources = ["School Newspaper", "School Newspaper", "Student Blog", "University Page", "University Page"]
for i in range(6,11):
    # Read the HTML file
    with open(f"intermediate_data/doc{i}.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Extract text
    parser = TextOnly()
    parser.feed(html)
    lines = parser.text

    # data cleaning
    # remove lines that are less than 5 words, likely buttons/side menus/nav bars
    filtered = [line.replace("\n", " ") for line in lines if len(line.split()) >4]

    # Join with newlines to roughly preserve paragraphs
    text = "\n\n".join(filtered)

    # # Write to a text file
    with open(f"documents/{file_sources[i-6]}_{file_titles[i-6]}.txt", "w", encoding="utf-8") as f:
        f.write(text)