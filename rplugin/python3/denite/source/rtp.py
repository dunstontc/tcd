"""A Denite source for Vim's runtime path."""
# ==============================================================================
#  FILE: rtp.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-26
# ==============================================================================

from .base import Base


class Source(Base):
    """A Denite source for Vim's runtime path."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'rtp'
        self.kind = 'directory'
        self.vars = {}

    def on_init(self, context):
        context['__paths'] = self.vim.call('eval', '&rtp ').split(',')

    def gather_candidates(self, context):
        candidates = []
        for path in context['__paths']:
            candidates.append({
                'word': path,
                'action__path': path,
            })

        return candidates

