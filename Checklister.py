# Checklist template: HTML and

def fill_template(content, holes):
    style = """<style type="text/css">
			html, body {
				padding: 0;
				margin: 0;
				font-family: "Verdana";
				font-size: 10pt;
			}
			.outline {
				border: 1px solid black;
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
				border-radius: calc(1ch + 3mm);
				width: 4.8in;
				height: 2.8in;	
				box-sizing: border-box;
				margin: 0.1in;
			}
			.hole {
				width: 6mm;
				height: 6mm;
				background-image: url("data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8' standalone='no'%3F%3E%3Csvg viewBox='0 0 8 8' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:svg='http://www.w3.org/2000/svg'%3E%3Cg%3E%3Cellipse style='fill:none;stroke:%23000000;stroke-width:0.626909;stroke-linecap:square;stop-color:%23000000' id='path846' cx='4' cy='4' rx='3.6865454' ry='3.6865456' /%3E%3Ccircle style='fill:%23000000;fill-opacity:1;stroke:none;stroke-width:1.01506;stroke-linecap:square;stop-color:%23000000' id='path950' cx='4' cy='4' r='0.5' /%3E%3C/g%3E%3C/svg%3E%0A");
				position: absolute;
				top: 0.2in
			}
			.left {
				left: 0.2in
			}
			.right {
				right: 0.2in		
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
		</style>"""
    return f"""
<!DOCTYPE html>
<html>
	<head>
	<meta http-equiv="content-type" content="text/html; charset=windows-1252">
		<title>Checklist</title>
		{style}
	</head>
	<body>
		<div class="outline">
			<div class="main">
				{'<div class="hole left"></div><div class="hole right"></div>' if holes else ""}
				{content}
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
    return markdown(md, extensions=[ChoiceTagExtension()])

## Main logic: parse Markdown files and spit out web pages

import argparse
from os.path import expanduser
from urllib.parse import quote
import webbrowser

parser = argparse.ArgumentParser(description='Create a checklist from Markdown')
parser.add_argument('filename', metavar='File', type=str, help='A Markdown file to render as a checklist')
parser.add_argument('--holes', dest='holes', action='store_const', const=True, default=False, help='Add indicators for hole punches')
args = parser.parse_args()

with open(expanduser(args.filename)) as f:
    html = mdChecklistToHTML(f.read())
    dataurl = "data:text/html," + quote(fill_template(html, args.holes))
    webbrowser.open_new(dataurl)
