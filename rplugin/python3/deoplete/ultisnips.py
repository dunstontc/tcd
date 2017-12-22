# ==============================================================================
#  FILE: ultisnips.py
#  AUTHORS: Alex LaFroscia & Herrington Darkholme
#  License: GPL v3.0
#  Last Modified: Jan 22, 2016
# ==============================================================================

from .base import Base

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'ultisnips'
        self.mark = '[US]'
        self.rank = 8

    def gather_candidates(self, context):
        suggestions = []
        snippets = self.vim.eval(
            'UltiSnips#SnippetsInCurrentScope()')
        for trigger in snippets:
            suggestions.append({
                'word': trigger,
                'menu': self.mark + ' ' + snippets.get(trigger, ''),
                'dup': 1
            })
        return suggestions
