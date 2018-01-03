# -*- coding: utf-8 -*-
# ==============================================================================
# FILE: mapping.py
# AUTHOR: Clay Dunston <dunstontc@gmail.com>
# License: MIT license
# Last Modified: 2018-01-03
# ==============================================================================

import re

from .base import Base


class Source(Base):

    def __init__(self, vim):

        super().__init__(vim)
        self.name = 'map_verbose'
        self.kind = 'mapping'
        self.commands = []

        # self.__re_command = re.compile(r'^\|:.+\|')
        # self.__re_tokens = re.compile(r'^\|:(.+)\|[\t\s]+:([^\t]+)[\t\s]+(.+)')

    def on_init(self, context):
        raw_maps          = self.vim.call('execute', 'verbose nmap')
        l_pattern         = re.compile(r'(^.*\n\t.*\n)', re.M)
        context['__mapz'] = l_pattern.split(raw_maps)
        # verbose_maps = self.vim.call('execute', 'verbose map')
        # thinned_maps = re.sub(r'(?m)^\t.*\n?', '', verbose_maps)
        # context['__mapz'] = thinned_maps.split('\n')
        # context['__verbose_pattern'] = re.compile(r'(^\S*)(?:\s*)(\S*)(?:\s*\*?\s?\:?)(.*$)')
        # mapping = []

    def gather_candidates(self, context):
        verbose_pattern = re.compile(r'(^\S*)(?:\s*)(\S*)(?:\s*\*?\@?\s?\@?)(.*$)', re.M)
        path_pattern    = re.compile(r'(?:/.*/.*/)(\S*/\S*/\S*\.\S*$)')
        candidates = []
        for maps in context['__mapz']:
            matches       = verbose_pattern.search(maps)
            clean_command = re.sub(r'(<\S*>)', r'\\\1', matches.group(3), 0)
            # cleaned_command = f'execute feedkeys(\"{clean_command}\", "n")'
            # path_match    = path_pattern.search(maps)
            if len(maps) > 1:
                candidates.append({
                    # 'word':             str(clean_command),
                    'word': 'execute "normal ' + matches.group(3) + '"',
                    'action__command': 'call feedkeys("' + clean_command + '")',
                    # 'action__command': matches.group(3),
                    # 'action__command': 'execute "normal ' + matches.group(3) + '"',
                    'abbr': '{0:<3} -- {1:<25} -- {2}'.format(
                        matches.group(1),
                        matches.group(2),
                        matches.group(3)),
                    })
        return candidates

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource_mapping /\v^.*$/ '
                         f'containedin={self.syntax_name} '
                         r'contains=deniteSource_mappingNoise,deniteSource_mappingMode,deniteSource_mappingLhs,deniteSource_mappingRhs')
        self.vim.command(r'syntax match deniteSource_mappingNoise /\(\s--\s\)/      contained ')
        self.vim.command(r'syntax match deniteSource_mappingMode  /^\s[nosvx]\+\s/  contained ')
        # self.vim.command(r'syntax match deniteSource_mappingLhs   /\(^.*--\s\zs.*\ze--\)/ contained ')
        self.vim.command(r'syntax match deniteSource_mappingRhs   /\v((-- .*){2})@<=(.*)/ contained ')

    def highlight(self):
        self.vim.command('highlight default link deniteSource_mapping      Normal')
        self.vim.command('highlight default link deniteSource_mappingNoise Comment')
        self.vim.command('highlight default link deniteSource_mappingMode  Identifier')
        self.vim.command('highlight default link deniteSource_mappingRhs   String')
        # self.vim.command('highlight default link deniteSource_mappingLhs   Identifier')

