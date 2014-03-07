from pydocx.DocxParser import DocxParser


class Docx2Markdown(DocxParser):

    def parsed(self):
        return self._parsed

    def escape(self, text):
        return text

    def linebreak(self):
        return '\n'

    def paragraph(self, text):
        return text + '\n'

    def heading(self, text, heading_level):
        return text

    def insertion(self, text, author, date):
        pass

    def hyperlink(self, text, href):
        return text        

    def image_handler(self, path):
        return path

    def image(self, path, x, y):
        return self.image_handler(path)

    def deletion(self, text, author, date):
        return text

    def bold(self, text):
        return '**' + text + '**'

    def italics(self, text):
        # TODO do we need a "pre" variable, so I can check for
        # *italics**italics* and turn it into *italicsitatlics*?
        return '*' + text + '*'

    def underline(self, text):
        return '***' + text + '***'
    
    def caps(self, text):
        return text

    def small_caps(self, text):
        return text

    def strike(self, text):
        return text

    def hide(self, text):
        return text
        
    def superscript(self, text):
        return text
    
    def subscript(self, text):
        return text
    
    def tab(self):
        return True
    
    def ordered_list(self, text):
        return text
    
    def unordered_list(self, text):
        return text
    
    def list_element(self, text):
        return text
    
    def table(self, text):
        return text
    
    def table_row(self, text):
        return text   

    def table_cell(self, text):
        return text
    
    def page_break(self):
        return True
    
    def indent(self, text, left='', right='', firstLine=''):
        return text




