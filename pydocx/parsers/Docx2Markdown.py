import base64, logging
import xml.sax.saxutils
from uuid import uuid4

from pydocx.DocxParser import DocxParser


class Docx2Markdown(DocxParser):

    def __init__(
            self,
            path,         
            convert_root_level_upper_roman=False,
            escape_text=False,
            pseudo_tab_indent=False,
            list_spacing=False,
            process_images=False,
            *args,
            **kwargs):
        self._images = {}
        self.md_tab = "&nbsp;&nbsp;&nbsp;&nbsp;" if escape_text else "\t" # 4 space indent
        self.escape_text = escape_text
        self.pseudo_tab_indent = pseudo_tab_indent
        self.list_spacing = list_spacing
        self.process_images = process_images
        super(Docx2Markdown, self).__init__(path, *args, **kwargs)

    @property
    def parsed(self):
        return self._parsed

    def escape(self, text):
        if self.escape_text:
            return xml.sax.saxutils.quoteattr(text)[1:-1]
        return text

    def linebreak(self, pre=None):
        return '  \n'

    def paragraph(self, text, pre=None):
        return text + '  \n'

    def heading(self, text, heading_value):
        print "HEADING: %s"%heading_value
        return text + '  \n'

    def insertion(self, text, author, date):
        pass

    def hyperlink(self, text, href):
        if text == '':
            return ''
        return '[%s](%s "%s")'%(text, href, text)

    def image_handler(self, image_data, filename):
        if self.process_images and image_data.strip():
            extension = filename.split('.')[-1].lower()
            data = base64.b64encode(image_data)

            image_id = int(uuid4().time_mid)
            self._images[image_id] = (extension, data)
            return image_id
        return ''

    # relies on backend to serve images
    def image(self, image_data, filename, x, y):

        if self.process_images:
            src = self.image_handler(image_data, filename)
            if not src:
                return ''
            src = "http://pydocx.appspot.com/img/%s" %src                            
            return '![Picture](%s)' % src       
        return ''

    @property
    def images(self):
        return self._images

    def deletion(self, text, author, date):
        return text

    def list_element(self, text):
        return '- ' + text + '  \n'

    def ordered_list(self, text, list_style):
        text = '\n'.join([line.replace('-',"%s."%i) for i, line in enumerate(text.splitlines(), 1)])
        text += '\n'
        if self.list_spacing:           
            text = '\n'+text+'\n[]()  \n' # spacing hack to make sure lists render properly
        return text

    def unordered_list(self, text):
        if self.list_spacing:
            text = '\n'+text+'\n[]()  \n' # spacing hack to make sure lists render properly
        return text

    def bold(self, text):
        # rather than stripping whitespace, move it outside of asterisks
        # can probably be better
        if text.strip():
            if text != text.rstrip():
                text = text.rstrip() + '** '
            else:
                text = text + '**'
            if text != text.lstrip():
                text = text.lstrip() + ' **'
            else:
                text = '**' + text
        return text

        # return '**' + text + '**'

    def italics(self, text):
        # TODO do we need a "pre" variable, so I can check for
        # *italics**italics* and turn it into *italicsitatlics*?

        # rather than stripping whitespace, move it outside of asterisks
        # can probably be better        
        if text.strip():
            if text != text.rstrip():
                text = text.rstrip() + '* '
            else:
                text = text + '*'
            if text != text.lstrip():
                text = text.lstrip() + ' *'
            else:
                text = '*' + text
        return text
        # return '*' + text.strip() + '*'

    def underline(self, text):
        # return '***' + text + '***'
        # conflicts w/ bold italic
        return text

    def caps(self, text):
        return text

    def small_caps(self, text):
        return text

    def strike(self, text):
        # rather than stripping whitespace, move it outside of asterisks
        # can probably be better        
        if text.strip():
            if text != text.rstrip():
                text = text.rstrip() + '~~ '
            else:
                text = text + '~~'
            if text != text.lstrip():
                text = text.lstrip() + ' ~~'
            else:
                text = '~~' + text
        return text

    def hide(self, text):
        return text

    def superscript(self, text):
        return text

    def subscript(self, text):
        return text

    def tab(self):
        # str.expandtabs()?
        text = ''
        if self.pseudo_tab_indent:
            text = self.md_tab + text
        return text

    def table(self, text):
        rows = text.splitlines()
        firstrow = rows[0]
        firstrowcells = firstrow.split('|')
        nocells = len(firstrowcells)-1
        headrow = '-----|'*(nocells)+'  '
        rows = [rows[0], headrow]+rows[1:]
        return '\n'.join(rows)+'  \n'
        # return text+'\n'

    def table_row(self, text):
        return text+'  \n'

    def table_cell(self, text, col='', row=''):
        return text+'|'

    def page_break(self):
        return '- - - -'

    def indent(self, text, just='', firstLine='', left='', right=''):
        # only left justified calculation for now
        if self.pseudo_tab_indent:

            tabno = 0

            if just == 'left' or not just:

                flno, lno = 0, 0

                if firstLine:
                    flpt = float(firstLine) * float(3) / float(4)
                    flno = int(flpt) / 36 # hardcoded?
                if left:
                    lpt = float(left) * float(3) / float(4)
                    lno = int(lpt) / 36 # hardcoded?

                tabno = flno + lno

                text = tabno*self.md_tab + text

        return text

    def break_tag(self):
        # expected paragraph?
        return '  \n'
