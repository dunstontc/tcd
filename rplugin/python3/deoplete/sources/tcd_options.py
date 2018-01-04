"""Deoplete source for Vim options."""
# ==============================================================================
#  FILE: tcd_options.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2018-01-03
# ==============================================================================


from json import load, JSONDecodeError

from .base import Base


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'tcd_options'
        self.mark = '[opt]'
        self.filetypes = ['vim']
        self.min_pattern_length = 1
        # self.data_dir = self.vim.eval('g:tcd#data_dir')

    def gather_candidates(self, context):
        candidates = []

        with open('/Users/clay/Projects/Vim/me/tcd/data/options.json', 'r') as fp:
            try:
                config = load(fp)
            except JSONDecodeError:
                config = []

            for obj in config:
                candidates.append({
                    'word': obj['option'],
                    # 'abbr': obj['shortname'],
                    'abbr': f"{obj['option']} ({obj['shortname']}) - {obj['description']}",
                })
        return candidates
