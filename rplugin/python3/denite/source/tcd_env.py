"""Denite source for environment variables."""
#  =============================================================================
#  FILE: env.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-26
#  =============================================================================

# import os

from .base import Base
# from denite import util


class Source(Base):
    """Denite source for environment variables."""

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'tcd_env'
        self.kind = 'word'
        self.vars = {}

    def on_init(self, context):
        """Collect all env variables."""
        context['variables'] = self.vim.call('tcd#Env')

    def gather_candidates(self, context):
        """Loop & return."""
        candidates = []

        for x in context['variables']:
            candidates.append({
                'word': f'${x}',
                'value': self.vim.call('expand', f'${x}').replace('\n', ','),
                'action__command': self.vim.call('expand', f'${x}'),
            })

        return self._convert(candidates)

    def _convert(self, candidates):
        """Format and add metadata to gathered candidates.

        Parameters
        ----------
        candidates : list

        Returns
        -------
        A sexy source.

        """
        word_len = self._get_length(candidates, 'word')

        for candidate in candidates:
            candidate['abbr'] = "{0:<{word_len}} -- {1}".format(
                candidate['word'],
                candidate['value'],
                word_len=word_len,
            )
        return candidates

    def _get_length(self, array, attribute):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_attr = item[attribute]
            cur_len = len(cur_attr)
            if cur_len > max_count:
                max_count = cur_len
        return max_count

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        self.vim.command(r'syntax match deniteSource_TCD_env /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_TCD_Var,deniteSource_TCD_Noise')
        self.vim.command(r'syntax match deniteSource_TCD_Noise /\s--\s/  contained ')
        self.vim.command(r'syntax match deniteSource_TCD_Var   /\$\S\+/  contained ')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        self.vim.command('highlight link deniteSource_TCD_env    Normal')
        self.vim.command('highlight link deniteSource_TCD_Noise  Comment')
        self.vim.command('highlight link deniteSource_TCD_Var    Boolean')

