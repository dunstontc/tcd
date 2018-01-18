# ============================================================================
# FILE: location_list.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# Editor: Clay Dunston <dunstontc@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
from .base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name     = 'tcd_loclist'
        self.kind     = 'file'
        self.syntax_name = 'deniteSource__LocationList'
        self.matchers = ['matcher_regexp']
        self.sorters  = []

    def on_init(self, context):
        context['__linenr']   = self.vim.current.window.cursor[0]
        context['__bufname']  = self.vim.current.buffer.name
        context['__bufnr']    = self.vim.current.buffer.number
        context['__filename'] = os.path.basename(context['__bufname'])

    def convert(self, val, context):
        type_str = 'Error' if val['type'].lower() == 'e' else 'Warning'
        bufnr    = val['bufnr']
        line     = val['lnum'] if bufnr != 0 else 0
        col      = val['col'] if bufnr != 0 else 0
        pos      = f"{line}:{col}"

        # TODO: What is this checking for?
        if len(context['__bufname']) == 0:
            word = val['text']
        else:
            word = f"{context['__filename']}  {pos:<6} │ {val['text']}"

        return {
            'word': word,
            'action__path': context['__bufname'],
            'action__line': line,
            'action__col':  col,
            'action__buffer_nr': context['__bufnr']
            }

    def gather_candidates(self, context):
        winnr = self.vim.eval('bufwinnr("' + context['__bufname'] + '")')
        items = self.vim.eval('getloclist(' + str(winnr) + ')')
        res = []
        for item in items:
            if item['valid'] != 0:
                res.append(self.convert(item, context))
        return res

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight default link {match["name"]} {match["link"]}')

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        self.vim.command(r'syntax match deniteSource__LocationList /^.*$/ containedin=' + self.syntax_name + ' contains='
                         r'deniteSource__LocationListPosition,'
                         r'deniteSource__LocationListString,'
                         r'deniteSource__LocationListNoise,'
                         r'deniteSource__LocationListFile,'
                         r'deniteSource__LocationListNum,'
                         r'deniteSource__LocationListErr,'
                         r'deniteSource__LocationListWarning')
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}{pattern['name']} {pattern['regex']}")

    # def define_syntax(self):
    #     """Define Vim regular expressions for syntax highlighting."""
    #     items = [x['name'] for x in SYNTAX_GROUPS]
    #     self.vim.command(r'syntax match deniteSource__LocationList /^.*$/ '
    #                      f"containedin={self.syntax_name} contains={','.join(items)}")
    #     for pattern in SYNTAX_PATTERNS:
    #         self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

SYNTAX_GROUPS = [
    {'name': 'deniteSource__LocationListNoise',    'link':  'Comment'},
    {'name': 'deniteSource__LocationListWarning',  'link':  'WarningMsg'},
    {'name': 'deniteSource__LocationListErr',      'link':  'Error'},
    {'name': 'deniteSource__LocationListName',     'link':  'Directory'},
    {'name': 'deniteSource__LocationListFile',     'link':  'Directory'},
    {'name': 'deniteSource__LocationListPosition', 'link':  'Number'},
    {'name': 'deniteSource__LocationListNum',      'link':  'Number'},
    {'name': 'deniteSource__LocationListString',   'link':  'String'},
]

SYNTAX_PATTERNS = [
    {'name': 'Header',   'regex':  r' /\v^.*\|\d.{-}\|/ contained containedin= deniteSource__LocationList'},
    {'name': 'Noise',    'regex':  r' /\( -- \)/        contained'},
    {'name': 'Noise',    'regex':  r' /\(│\)/           contained'},
    {'name': 'Noise',    'regex':  r' /\(\d\)\@<=\(:\)/ contained containedin=deniteSource__LocationListPosition'},
    {'name': 'Position', 'regex':  r' /\s\d\+:\d\+\s/   contained'},
    {'name': 'File',     'regex':  r' /^\s\+\S\+\s/     contained'},
    {'name': 'Num',      'regex':  r' /\d/              contained'},
    {'name': 'String',   'regex':  r' /\s".*"/          contained'},
    {'name': 'String',   'regex':  r" /\s'.*'/          contained"},
    {'name': 'String',   'regex':  r" /\s`.*`/          contained"},
    {'name': 'Err',      'regex':  r' /\v(\s|\()@<=[DEFUW]\d+/  contained'},
    {'name': 'Err',      'regex':  r' /\v(\s|\()@<=CS\d+/  contained'},
    # {'name': 'Err',     'regex':  r' /\v([A-Z][a-z]+)+Error.*/ contained'},
    {'name': 'Warning',      'regex':  r' /\((\)\@<=\w\+\()$\)\@=/  contained'},
    # {'name': 'Err',      'regex':  r' /Error/           contained containedin=deniteSource__LocationListPosition'},
    # {'name': 'Warning',  'regex':  r' /Warning/         contained containedin=deniteSource__LocationListPosition'},
]

#  tcd_loclist.py  11:1   │ E302 expected 2 blank lines, found 1 (errcheck)
#  tcd_loclist.py  11:1   │ D101 Missing docstring in public class (errcheck)
#  tcd_loclist.py  13:1   │ D107 Missing docstring in __init__ (errcheck)
#  tcd_loclist.py  21:1   │ D102 Missing docstring in public method (errcheck) (errcheck)
#  tcd_loclist.py  27:1   │ D102 Missing docstring in public method
#  tcd_loclist.py  28:9   │ F841 local variable 'type_str' is assigned to but never used
#  tcd_loclist.py  46:13  │ E123 closing bracket does not match indentation of opening bracket's line
#  tcd_loclist.py  48:1   │ D102 Missing docstring in public method
#  tcd_loclist.py  64:121 │ E501 line too long (121 > 120 characters)
#  tcd_loclist.py  83:1   │ E305 expected 2 blank lines after class or function definition, found 1
