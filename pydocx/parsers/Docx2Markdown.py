import base64
import xml.sax.saxutils

from pydocx.DocxParser import DocxParser


class Docx2Markdown(DocxParser):

    def __init__(
            self,
            path,
            for_html=False,            
            convert_root_level_upper_roman=False,
            *args,
            **kwargs):
        self._for_html = for_html
        super(Docx2Markdown, self).__init__(path, *args, **kwargs)

    @property
    def for_html(self):
        return self._for_html

    @property
    def parsed(self):
        return self._parsed

    def escape(self, text): #?
        if self.for_html:
            return xml.sax.saxutils.quoteattr(text)[1:-1]
        return text

    def linebreak(self, pre=None):
        return '  \n'

    def paragraph(self, text, pre=None):
        return text + '  \n'

    def heading(self, text, heading_value):
        print "HEADING: %s"%heading_value
        return text

    def insertion(self, text, author, date):
        pass

    def hyperlink(self, text, href):
        return text

    def image_handler(self, image_data, filename):
        return text

    # def image_handler(self, path):
    #     return path

    def image(self, image_data, filename, x, y):
        return text

    # def image(self, path, x, y):
    #     return self.image_handler(path)        

    def deletion(self, text, author, date):
        return text

    def list_element(self, text):
        return text

    def ordered_list(self, text, list_style):
        return text

    def unordered_list(self, text):
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
        # Insert before the text right?? So got the text and just do an insert
        # at the beginning!
        if self.for_html:
            text = '&nbsp;&nbsp;&nbsp;&nbsp;' + text
        return text

    def table(self, text):
        return text

    def table_row(self, text):
        return text

    def table_cell(self, text, col='', row=''):
        return text

    def page_break(self):
        return '-----------------------'

    def indent(self, text, just='', firstLine='', left='', right=''):
        if self.for_html:
            text = '&nbsp;&nbsp;&nbsp;&nbsp;' + text
        return text

    def break_tag(self):
        return ''
