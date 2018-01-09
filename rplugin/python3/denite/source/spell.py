"""A denite source for spellfiles."""
# ==============================================================================
#  FILE: spell.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2018-01-09
# ==============================================================================


# It's easiest to extend an existing source,
# or at least the Base class.
from .base import Base

# from denite.util import error


class Source(Base):
    """Describe the purpose of our source."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'spell'
        self.kind = 'word'
        self.syntax_name = 'deniteSource_spell'
        self.vars = {
            'spellfile': vim.eval('&spellfile')
        }

    def on_init(self, context):
        """Check that the user has defined &spellfile."""
        context['__spellfile'] = self.vim.eval('&spellfile')
        # if not len(self.vars['spellfile']):
        with open(self.vars['spellfile'], 'r') as splf:
            # FIXME: W18: Invalid character in group name
            context['__spell_words'] = splf.read().split('\n')

    def gather_candidates(self, context):
        """Fill a list with the candidates and send them onward."""
        candidates = []

        for item in context['__spell_words']:
            if len(item):
                candidates.append({
                    'word': item.rstrip('\n')
                })
        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(r'syntax match {self.syntax_name} /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight default link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    {'name': 'deniteSource_spell',       'link': 'Normal' },
    {'name': 'deniteSource_spell_Noise', 'link': 'Comment'},
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',  'regex':  r' /\( -- \)/  contained'},
]

