"""Let's interact with Ultisnips."""
# ============================================================================
# FILE:    ultisnips.py
# AUTHOR:  Clay Dunston <dunstontc@gmail.com>
# License: MIT license
# Last Modified: 2017-12-26
# ============================================================================

from os import listdir
from os.path import isfile

from .base import Base
from denite.util import expand

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'ultisnips_file'
        self.matchers = ['matcher_regexp']
        self.kind = 'file'
        self.vars = {
            'snippets_dirs': vim.vars.get('UltiSnipsSnippetDirectories'),
            'snippets_dir':  vim.vars.get('UltiSnipsSnippetsDir'),
            'snippets_path': vim.vars.get('tcd#snippets_path'),
        }

    def on_init(self, context):
        if self.vars['snippets_path']:
            context['__snip_dir'] = self.vars['snippets_path']
        # elif context['snippets_dirs']:
        #     if self.vars['snippets_dirs']
        # else:
        #     __snip_dir = self.vars['snippets_dir'][0]
        #     context['__snip_dir'] = expand('~/.config/nvim', __snip_dir)

        context['__snip_files'] = [f for f in listdir(context['__snip_dir']) if isfile(f)]



    def gather_candidates(self, context):
        candidates = []
        for item in context['__snip_files']:
            candidates.append({
                'word': expand(context['__snip_dir'], item)
                # 'action__path': obj['path'],
            })

        return candidates

    def _get_width(self, array, attribute):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_attr = item[attribute]
            cur_len = len(cur_attr)
            if cur_len > max_count:
                max_count = cur_len
        return max_count

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_TCD /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_TCD_Noise,deniteSource_TCD_Key')
        self.vim.command(r'syntax match  deniteSource_TCD_Noise  /\(\s--\s\)/                 contained')
        self.vim.command(r'syntax match  deniteSource_TCD_Key    /^\(.*\)\(\( -- .*\)\)\@=/   contained')


    def highlight(self):
        self.vim.command('highlight link deniteSource_TCD        Normal')
        self.vim.command('highlight link deniteSource_TCD_Noise  Comment')
        self.vim.command('highlight link deniteSource_TCD_Key    Identifier')
