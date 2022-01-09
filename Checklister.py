# Checklist template: HTML and CSS

topTemplate = """
<!DOCTYPE html>
<html>
<head>
	<title>Checklist</title>
	<style type="text/css">
		html, body {
			padding: 0;
			margin: 0;
			font-family: "Verdana";
			font-size: 10pt;
		}
		.outline {
			border-right: 1px solid black;
			border-bottom: 1px solid black;
			width: 5in;
			height: 3in;
			position: absolute;
			top: 0;
			left: 0;
		}
		.main {
			border: 1ch solid black;
			padding: 1ch;
			padding-top: 0ch;
			border-radius: 3ch;
			width: 4.8in;
			height: 2.8in;	
			box-sizing: border-box;
			margin: 0.1in;
		}
		ul {
			padding-left: 15px;
		}
		li {
			padding-inline-start: 1ch;
			line-height: 1.5;
			list-style-type: "\\2610";
		}
		ul li ul li {
			list-style-type: "\\25A0";
		}
		span {
			font-weight: bold;
			background-color: lightgray;
			border-radius: 3px;
			padding-left: 3px;
			padding-right: 3px;
		}
	</style>
</head>
<body>
	<div class="outline">
		<div class="main">
"""

bottomTemplate = """
		</div>
	</div>
</body>
</html>
"""

# Extending Markdown to support ??...?? spans

from markdown import markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension

class ChoiceTagExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(SimpleTagInlineProcessor(r'()\?\?(.*?)\?\?', 'span'), 'choice_tag', 175)

def mdChecklistToHTML(md):
    return topTemplate + markdown(md, extensions=[ChoiceTagExtension()]) + bottomTemplate

## Main logic: parse Markdown files and spit out web pages

import sys
from urllib.parse import quote
import webbrowser

with open(sys.argv[1]) as f:
    html = mdChecklistToHTML(f.read())
    dataurl = "data:text/html," + quote(html)
    webbrowser.open_new(dataurl)
