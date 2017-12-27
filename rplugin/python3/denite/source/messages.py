"""A Denite source for `:messages`."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-26
# ==============================================================================

from .base import Base

SYNTAX_GROUPS = [
    {'name': 'deniteSource_Messages',         'link': 'Normal' },
    {'name': 'deniteSource_Messages_Noise',   'link': 'Comment'},
    {'name': 'deniteSource_Messages_Origin',  'link': 'Type'   },
    {'name': 'deniteSource_Messages_String',  'link': 'String' },
    {'name': 'deniteSource_Messages_Command', 'link': 'PreProc'},
    {'name': 'deniteSource_Messages_Err',     'link': 'Error'  },
    {'name': 'deniteSource_Messages_Num',     'link': 'Number' },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',   'regex':  r' /\( -- \)/    contained'},
    {'name': 'Noise',   'regex':  r' /\(File\)/    contained'},
    {'name': 'Origin',  'regex':  r' /^\s(.*)\s/   contained'},
    {'name': 'Origin',  'regex':  r' /^\s\[.*\]\s/ contained'},
    {'name': 'String',  'regex':  r' /\s".*"/      contained'},
    {'name': 'String',  'regex':  r" /\s'.*'/      contained"},
    {'name': 'Command', 'regex':  r' /\s:\w*\s\ze/ contained'},
    {'name': 'Command', 'regex':  r' /\s:\w*$/     contained'},
    {'name': 'Err',     'regex':  r' /[DEFW]\d\+/  contained'},
    {'name': 'Err',     'regex':  r' /TypeError/   contained'},
    {'name': 'Err',     'regex':  r' /KeyError/    contained'},
    {'name': 'Err',     'regex':  r' /ValueError/  contained'},
    {'name': 'Num',     'regex':  r' /\d/          contained'},
]


class Source(Base):
    """Make it easier to see our messages."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'messages'
        self.syntax_name = 'deniteSource_Messages'
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
                candidates.insert(0, {'word': item})
        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(r'syntax match deniteSource_Messages /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight default link {match["name"]} {match["link"]}')

