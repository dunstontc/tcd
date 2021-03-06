"""A Denite source for `:messages`."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  LICENSE: MIT License
#  Last Modified: 2018-01-05
# ==============================================================================

from .base import Base


class Source(Base):
    """Make it easier to see our messages."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'messages'
        self.syntax_name = 'deniteSource__Messages'
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
            if len(item) > 1:
                count -= 1
                candidates.insert(0, {'word': f'{str(count):>2}│ {item}'})
                # candidates.append({'word': str(context['msg_count'])})
        return candidates

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'hi default link {match["name"]} {match["link"]}')

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(r'syn match deniteSource__Messages /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syn match {self.syntax_name}_{pattern['name']} {pattern['regex']}")
            self.vim.command(r"syn region deniteSource__Messages_String start=+'+ end=+'+")
            self.vim.command(r'syn region deniteSource__Messages_String start=+"+ end=+"+')
            self.vim.command(r'syn region deniteSource__Messages_String start=+`+ end=+`+')


SYNTAX_GROUPS = [
    {'name': 'deniteSource__Messages',         'link': 'Normal'   },
    {'name': 'deniteSource__Messages_Noise',   'link': 'Comment'  },
    {'name': 'deniteSource__Messages_Origin',  'link': 'Comment'  },
    {'name': 'deniteSource__Messages_String',  'link': 'String'   },
    {'name': 'deniteSource__Messages_Path',    'link': 'Directory'},
    {'name': 'deniteSource__Messages_Command', 'link': 'Type'  },
    {'name': 'deniteSource__Messages_Err',     'link': 'Error'    },
    {'name': 'deniteSource__Messages_Num',     'link': 'Number'   },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',   'regex':  r' /\( -- \)/                 contained'},
    {'name': 'Noise',   'regex':  r' /\s\s\(File\)/             contained'},
    {'name': 'Noise',   'regex':  r' /\zs│\ze/                  contained'},
    # {'name': 'Origin',  'regex':  r' /^\s\+\d\+│\s\[\S\+\]\s/  contained contains=deniteSource__Messages_Noise,deniteSource__Messages_Num'},
    {'name': 'Origin',  'regex':  r' /^\s\+\d\+│\s\[\S\+\]\s/  contained contains=deniteSource__Messages_Noise'},
    {'name': 'Path',    'regex':  r' /\s"\/.*"/                 contained'},
    {'name': 'Path',    'regex':  r' /\d\+\(L\|C\)/             contained contains=deniteSource__Messages_Num'},
    {'name': 'Command', 'regex':  r' /\s:\w*\s\ze/              contained'},
    {'name': 'Command', 'regex':  r' /\[W\]/                    contained'},
    {'name': 'Err',     'regex':  r' /\s[DEFW]\d\+/             contained'},
    {'name': 'Err',     'regex':  r' /WARNING:/                 contained'},
    {'name': 'Err',     'regex':  r' /\v([A-Z][a-z]+)+Error.*/  contained contains=deniteSource__Messages_String'},
    {'name': 'Num',     'regex':  r' /\d/                       contained'},
    {'name': 'Num',     'regex':  r' /\d\+[CL]/                 contained'},
]
