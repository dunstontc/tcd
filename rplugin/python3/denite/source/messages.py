"""A Denite source for `:messages`."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  LICENSE: MIT License
#  Last Modified: 2017-12-31
# ==============================================================================

from .base import Base

SYNTAX_GROUPS = [
    {'name': 'deniteSource_Messages',         'link': 'Normal'   },
    {'name': 'deniteSource_Messages_Noise',   'link': 'Comment'  },
    {'name': 'deniteSource_Messages_Origin',  'link': 'Comment'  },
    {'name': 'deniteSource_Messages_String',  'link': 'String'   },
    {'name': 'deniteSource_Messages_Path',    'link': 'Directory'},
    {'name': 'deniteSource_Messages_Command', 'link': 'PreProc'  },
    {'name': 'deniteSource_Messages_Err',     'link': 'Error'    },
    {'name': 'deniteSource_Messages_Num',     'link': 'Number'   },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',   'regex':  r' /\( -- \)/                contained'},
    {'name': 'Noise',   'regex':  r' /\s\{2}\(File\)/          contained'},
    {'name': 'Origin',  'regex':  r' /^\s(.*)\s/               contained'},
    {'name': 'Origin',  'regex':  r' /^\s\+\d\+\|\s\[\S\+\]\s/ contained'},
    {'name': 'String',  'regex':  r' /\s".*"/                  contained'},
    {'name': 'String',  'regex':  r" /\%(\[\)\@<='.*'\%(]\)\@=/ contained"},
    {'name': 'Path',    'regex':  r' /\s"\/.*"/                contained'},
    {'name': 'String',  'regex':  r" /\s'.*'/                  contained"},
    {'name': 'Command', 'regex':  r' /\s:\w*\s\ze/             contained'},
    {'name': 'Command', 'regex':  r' /\s:\w*$/                 contained'},
    {'name': 'Err',     'regex':  r' /\s[DEFW]\d\+/            contained'},
    {'name': 'Err',     'regex':  r' /\v([A-Z][a-z]+)+Error.*/ contained'},
    {'name': 'Num',     'regex':  r' /\d/                      contained'},
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
        context['msg_count'] = len(list(context['__messages']))

    def gather_candidates(self, context):
        """And send the messages onward."""
        candidates = []
        count = context['msg_count']
        for item in context['__messages']:
            if len(item):
                count -= 1
                candidates.insert(0, {'word': f'{str(count):>2}│ {item}'})
                # candidates.append({'word': str(context['msg_count'])})
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

