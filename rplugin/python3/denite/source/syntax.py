"""A Denite source for syntax highlighting groups."""
# ==============================================================================
#  FILE: syntax.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-23
# ==============================================================================

import re

from .base import Base


class Source(Base):
    """Make it easier to see our syntaxes."""

    def __init__(self, vim):
        """Character creation."""
        super().__init__(vim)

        self.name = 'syntax'
        self.kind = 'word'
        self.vars = {}

    def on_init(self, context):
        """Capture ``:syntax``."""
        context['__scopes'] = self.vim.call('execute', 'syntax').split('\n')

    def gather_candidates(self, context):
        """And send the candidates onward."""
        candidates = []
        syntax_pattern = re.compile(r'^\w+')

        for item in context['__scopes']:
            scoop = syntax_pattern.match(item)
            if not str(scoop) == 'None':
                candidates.append({
                    'word': scoop.group(0)
                })

        self.vars['__scopes'] = candidates
        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['word'] for x in self.vars['__scopes']]
        # self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
        #                  f'containedin={self.syntax_name} contains={",".join(items)}')
        for y in items:
            items = [x['word'] for x in self.vars['__scopes']]
            self.vim.command(f'syntax keyword {y} {y} ')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for x in self.vars['__scopes']:
            self.vim.command(f'highlight link {x["word"]} {x["word"]}')
