"""A Denite source for Vim variables."""
# ==============================================================================
#  FILE: var.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-24
# ==============================================================================

import re

from .base import Base

search_pattern = re.compile(r'^(\S+)\s+(.*)$', re.M)


def get_width(array, attribute):
    """Get the max string length for an attribute in a collection."""
    max_count = int(0)
    for item in array:
        cur_attr = item[attribute]
        cur_len = len(cur_attr)
        if cur_len > max_count:
            max_count = cur_len
    return max_count


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'var'
        self.kind = 'word'
        self.vars = {}

    def on_init(self, context):
        context['__vars'] = self.vim.call('execute', 'let ').split('\n')

    def gather_candidates(self, context):
        candidates = []
        for item in context['__vars']:
            matches = search_pattern.search(item)
            if matches:
                candidates.append({
                    'word': matches.group(1),
                    '__description': matches.group(2)
                })

        var_len = get_width(candidates, 'word')

        for candidate in candidates:
            candidate['abbr'] = "{0:<{var_len}} -- {1}".format(
                candidate['word'],
                candidate['__description'],
                var_len=var_len
            )
        return candidates

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_TCD /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_TCD_Noise,deniteSource_TCD_Var,deniteSource_TCD_Num,deniteSource_TCD_String,deniteSource_TCD_Other,deniteSource_TCD_Map,deniteSource_TCD_Punc')
        self.vim.command(r'syntax match  deniteSource_TCD_Noise  /\(\s--\s\)/                 contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Noise  /\(#\)/                      contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Punc  /[\[\]{}:,\*]/                contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Map    /<.\+>/                      contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Var    /^\(.*\)\(\( -- .*\)\)\@=/   contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Num    /\d/                         contained')
        self.vim.command(r"syntax region deniteSource_TCD_String start=/'/ end=/'\|$/         contained oneline")



    def highlight(self):
        self.vim.command('highlight link deniteSource_TCD        Normal')
        self.vim.command('highlight link deniteSource_TCD_Noise  Comment')
        self.vim.command('highlight link deniteSource_TCD_Var    Identifier')
        self.vim.command('highlight link deniteSource_TCD_Num    Number')
        self.vim.command('highlight link deniteSource_TCD_String String')
        self.vim.command('highlight link deniteSource_TCD_Other  Type')
        self.vim.command('highlight link deniteSource_TCD_Map    Type')
        self.vim.command('highlight link deniteSource_TCD_Punc   PreProc')
