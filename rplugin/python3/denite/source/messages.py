"""A Denite source for `:messages`."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  Last Modified: 2017-12-21
# ==============================================================================

from .base import Base


class Source(Base):
    """Make it easier to see our messages."""

    def __init__(self, vim):
        """Character creation."""
        super().__init__(vim)

        self.name = 'messages'
        self.kind = 'word'
        self.vars = {}

    def on_init(self, context):
        """Capture `:messages`."""
        context['__messages'] = self.vim.call('execute', 'messages').split('\n')

    def gather_candidates(self, context):
        """And send the messages onward."""
        candidates = []
        for item in context['__messages']:
            candidates.append({
                # 'word': 'test',
                'word': item
                # 'abbr': str(item.values())
                # join(item.values()[1])
            })
        return candidates

    def define_syntax(self):
        """Make the messages pretty."""
        self.vim.command(r'syntax match deniteSource_Messages /^.*$/ containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Messages_Origin,deniteSource_Messages_String,deniteSource_Messages_Command')
        self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s(.*)\s/   contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s\[.*\]\s/ contained ')
        self.vim.command(r'syntax match deniteSource_Messages_String   /\s".*"/      contained ')
        self.vim.command(r"syntax match deniteSource_Messages_String   /\s'.*'/      contained ")
        self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*\s\ze/ contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*$/     contained ')

    def highlight(self):
        """Make the messages pretty."""
        self.vim.command('highlight default link deniteSource_Messages         Normal')
        self.vim.command('highlight default link deniteSource_Messages_Origin  Type')
        self.vim.command('highlight default link deniteSource_Messages_String  String')
        self.vim.command('highlight default link deniteSource_Messages_Command PreProc')
