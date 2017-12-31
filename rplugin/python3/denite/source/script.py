"""A Denite source for loaded scripts."""
# ==============================================================================
#  FILE: script.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-31
# ==============================================================================


from .base import Base


class Source(Base):
    """Make it easier to see the scripts we've loaded."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'script'
        self.kind = 'word'
        self.syntax_name = 'deniteSource_Script'
        self.vars = {}

    def on_init(self, context):
        """Capture ``:syntax``."""
        context['__scrips'] = self.vim.call('execute', 'script').split('\n')

    def gather_candidates(self, context):
        """And send the candidates onward."""
        candidates = []

        for item in context['__scrips']:
            if len(item) > 1:
                candidates.append({
                    'word': item
                })
        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(r'syntax match deniteSource_Script /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight default link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    {'name': 'deniteSource_Script',      'link': 'Normal'    },
    {'name': 'deniteSource_Script_Num',  'link': 'Number'    },
    {'name': 'deniteSource_Script_File', 'link': 'Directory' },
]

SYNTAX_PATTERNS = [
    {'name': 'File', 'regex': r' /\%(\/\)\@<=\(\w\|-\)\+\.vim\(\s\|$\)/ contained'},
    {'name': 'Num',  'regex': r' /\d\+:\ze/                             contained'},
]

