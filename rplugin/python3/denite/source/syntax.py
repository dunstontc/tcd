"""A Denite source for `:syntax`."""
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
        """Capture `:syntax`."""
        context['__messages'] = self.vim.call('execute', 'syntax').split('\n')

    def gather_candidates(self, context):
        """And send the candidates onward."""
        candidates = []
        syntax_pattern = re.compile(r'^\w+')

        for item in context['__messages']:
            scoop = syntax_pattern.match(item)
            if not str(scoop) == 'None':
                candidates.append({
                    'word': scoop.group(0)
                })
        return candidates


