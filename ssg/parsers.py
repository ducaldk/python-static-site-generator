from typing import List
from pathlib import Path
import shutil
import sys
from docutils.core import publish_parts
from markdown import markdown
from ssg.content import Content

class Parser:
    extensions: List[str] = []

    def valid_extension(self, extension):
        return extension in self.extensions

    def parse(self, path:Path, source:Path, dest:Path):
        raise NotImplementedError
        # do not add the message argument - they don't like it

    def read(self, path):
        with open(path, "r") as file:
            return file.read()
    
    def write(self, path, dest, content, ext=".html"):
        full_path = dest / path.with_suffix(ext=ext).name
        with open(full_path, "w") as file:
            file.write(content)

    def copy(self, path, source, dest):
        shutil.copy2(path, dest / path.relative_to(source))
    

class ResourceParser(Parser):

    extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    def parse(self, path:Path, source:Path, dest:Path):
        self.copy(path, source, dest)
        # recall that 'self' is magically added

    
class MarkdownParser(Parser):
    extensions = [ ".md", ".markdown" ]

    # directions for this are sort of in reverse polish notation
    # or 'unhelpful' bomb defusing steps, like 'but first, cut the red wire'
    def parse(self, path:Path, source:Path, dest:Path) :
        content = Content.load(self.read(path))
        html = markdown(content.body)
        self.write(path, dest, html)
        # this test was space-sensitive, and I had two spaces after 'HTML.'
        sys.stdout.write("\x1b[1;32m{} converted to HTML. Metadata: {}\n".format(path.name, content))

class ReStructuredTextParser(Parser):
    extensions = [".rst"]

    def parse(self, path:Path, source:Path, dest:Path):
        content = Content.load(self.read(path))
        html = publish_parts(content.body, writer_name="html5")
        # ah, this had to be html_body, not just cut and paste...
        self.write(path, dest, html["html_body"])
        # again, space-sensitive
        sys.stdout.write("\x1b[1;32m{} converted to HTML. Metadata: {}\n".format(path.name,content))
    