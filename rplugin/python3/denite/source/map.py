# -*- coding: utf-8 -*-
# ==============================================================================
# FILE: mappings.py
# AUTHOR: Clay Dunston <dunstontc at gmail.com>
# License: MIT license
# ==============================================================================

from .base import Base # Base Denite class
import re              # regex

# MAPPINGS_HIGHLIGHT_SYNTAX = [
#     {'name': 'Mode', 'link': 'String', 're': '^\w\+'},
#     {'name': 'Lhs',  'link': 'String', 're': '(^\S*\s*)(\S*)'},
#     {'name': 'Rhs',  'link': 'String', 're': '(?:^\S*\s*\S*\s*\*?\s?\:?)(.*$)'},
# ]

class Source(Base):

    def __init__(self, vim):

        super().__init__(vim)
        self.name = 'map'
        self.kind = 'command'
        # self.syntax_name = 'deniteSource__Mappings'
        self.matchers = ['matcher_fuzzy']
        self.sorters = ['sorter_rank']

    def on_init(self, context):
        # context['__rawmaps'] = self.vim.call('execute', 'nmap').split('\n')
        verbose_maps = self.vim.call('execute', 'verbose map')
        thinned_maps = re.sub(r'(?m)^\t.*\n?', '', verbose_maps)
        context['__mapz'] = thinned_maps.split('\n')
        context['__verbose_pattern'] = re.compile(r'(^\S*)(?:\s*)(\S*)(?:\s*\*?\s?\:?)(.*$)')
        # mappings = []

    def gather_candidates(self, context):
        candidate = []
        for maps in context['__mapz']:
            matches = context['__verbose_pattern'].search(maps)
            if len(maps):
                candidate.append({
                    'word': maps,
                    'abbr': maps,
                    'action__command': matches.group(3),
                    # 'action__text': matches.group(3)
                })
        return candidate

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource_Mappings /\v^.*$/ containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource_MappingsNoise /\(\s\?\*\s\)\|\(\*@\)\|\(\s\{3\}@\)/ contained '
                         r'contained containedin=deniteSource_Mappings')
        self.vim.command(r'syntax match deniteSource_MappingsMode /^\s\w\+/ contained '
                         r'contained containedin=deniteSource_MappingsLhs')
        self.vim.command(r'syntax match deniteSource_MappingsLhs /\(^\s\S*\s*\)\(\S*\)/ contained '
                         r'contained containedin=deniteSource_Mappings')
        # self.vim.command(r'syntax match deniteSource_MappingsRhs /(?:^\s\S*\s*\S*\s*\*?\s?\:?)(.*$)/ contained '
                         # r'contained containedin=deniteSource_Mappings')

    def highlight(self):
        self.vim.command('highlight default link deniteSource_Mappings Function')
        self.vim.command('highlight default link deniteSource_MappingsNoise Comment')
        self.vim.command('highlight default link deniteSource_MappingsMode Comment')
        self.vim.command('highlight default link deniteSource_MappingsLhs Identifier')
        # self.vim.command('highlight default link deniteSource_MappingsRhs Function')
