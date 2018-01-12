# ============================================================================
# FILE: quickfix.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# Editor: Clay Dunston <dunstontc@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import re
from .base import Base

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name     = 'tcd_quickfix'
        self.kind     = 'file'
        self.syntax_name = 'deniteSource_Quickfix'
        self.matchers = ['matcher_fuzzy']
        self.sorters  = []

    # def define_syntax(self):
    #     self.vim.command('syntax case ignore')
    #     self.vim.command(r'syntax match deniteSource_QuickfixHeader   /\v^.*$/ '
    #                      r'containedin=' + self.syntax_name + ' '
    #                      r'contains=deniteSource_QuickfixName,deniteSource_QuickfixPosition')
    #
    #     self.vim.command(r'syntax match deniteSource_QuickfixName     /\v^[^|]+/ contained ')
    #     self.vim.command(r'syntax match deniteSource_QuickfixPosition /\v\|\zs.{-}\ze\|/ contained ')
    #
    #     word = self.vim.eval('get(g:,"grep_word", "")')
    #     if word:
    #         pattern = re.escape(word)
    #         self.vim.command(r'syntax match deniteSource_QuickfixWord /%s/' % pattern)
    #
    # def highlight(self):
    #     self.vim.command('highlight default link deniteSource_QuickfixWord     Search')
    #     self.vim.command('highlight default link deniteSource_QuickfixName     Directory')
    #     self.vim.command('highlight default link deniteSource_QuickfixPosition Comment')


    def convert(self, val, context):
        bufnr = val['bufnr']
        line  = val['lnum'] if bufnr != 0 else 0
        col   = val['col'] if bufnr != 0 else 0
        fname = "" if bufnr == 0 else self.vim.eval('bufname(' + str(bufnr) + ')')

        word  = '{fname} |{location}| {text}'.format(
            fname=fname,
            location='' if line == 0 and col == 0 else '%d col %d' % (line, col),
            text=val['text']
        )

        return {
            'word':              word,
            'action__path':      fname,
            'action__line':      line,
            'action__col':       col,
            'action__buffer_nr': bufnr,
        }

    def gather_candidates(self, context):
        items = self.vim.eval('getqflist()')
        res = []

        for item in items:
            if item['valid'] != 0:
                res.append(self.convert(item, context))
        return res

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight default link {match["name"]} {match["link"]}')

    # def define_syntax(self):
    #     """Define Vim regular expressions for syntax highlighting."""
    #     self.vim.command(r'syntax match deniteSource__LocationList /^.*$/ containedin=' + self.syntax_name + ' contains='
    #                      r'deniteSource__LocationListPosition,'
    #                      r'deniteSource__LocationListString,'
    #                      r'deniteSource__LocationListNoise,'
    #                      r'deniteSource__LocationListFile,'
    #                      r'deniteSource__LocationListNum,'
    #                      r'deniteSource__LocationListErr,'
    #                      r'deniteSource__LocationListWarning')
    #     for pattern in SYNTAX_PATTERNS:
    #         self.vim.command(f"syntax match {self.syntax_name}{pattern['name']} {pattern['regex']}")

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(r'syntax match deniteSource__LocationList /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

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
    # {'name': 'Err',     'regex':  r' /\v([A-Z][a-z]+)+Error.*/ contained'},
    # {'name': 'Err',      'regex':  r' /Error/           contained containedin=deniteSource__LocationListPosition'},
    # {'name': 'Warning',  'regex':  r' /Warning/         contained containedin=deniteSource__LocationListPosition'},
]

