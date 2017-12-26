"""A Denite source for `:messages`."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-26
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
            if len(item):
                candidates.insert(0, {
                    'word': item,
                })
        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        self.vim.command(r'syntax match deniteSource_Messages /^.*$/ containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Messages_Origin,deniteSource_Messages_String,deniteSource_Messages_Command,deniteSource_Messages_Err,deniteSource_Messages_Err,deniteSource_Messages_Noise')
        self.vim.command(r'syntax match deniteSource_Messages_Noise    /\( -- \)/       contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Noise    /\(File\)/       contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s(.*)\s/      contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s\[.*\]\s/    contained ')
        self.vim.command(r'syntax match deniteSource_Messages_String   /\s".*"/         contained ')
        self.vim.command(r'syntax match deniteSource_Messages_String   /\s".*"/         contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*\s\ze/    contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*$/        contained ')
        self.vim.command(r'syntax match deniteSource_Messages_Err      /[DEFW]\d\+/     contained ')
        self.vim.command(r"syntax match deniteSource_Messages_Num      /\d/             contained ")

    def highlight(self):
        """Define Vim regular expressions for syntax highlighting."""
        self.vim.command('highlight default link deniteSource_Messages         Normal')
        self.vim.command('highlight default link deniteSource_Messages_Noise   Comment')
        self.vim.command('highlight default link deniteSource_Messages_Origin  Type')
        self.vim.command('highlight default link deniteSource_Messages_String  String')
        self.vim.command('highlight default link deniteSource_Messages_Command PreProc')
        self.vim.command('highlight default link deniteSource_Messages_Err     Error')
        self.vim.command('highlight default link deniteSource_Messages_Num     Number')
