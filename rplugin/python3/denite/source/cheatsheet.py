"""A template for denite source files."""
# ==============================================================================
#  FILE: cheatsheet.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2018-01-02
# ==============================================================================


from json import dump, load, JSONDecodeError
from os.path import exists, expanduser, isfile

from .base import Base
from denite.util import error, expand


class Source(Base):
    """Describe the purpose of our source."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'cheatsheet'
        self.kind = 'word'
        self.syntax_name = 'deniteSource_cheatsheet'
        self.vars = {
            'data_dir':     vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'icon_setting': vim.vars.get('projectile#enable_devicons'),
        }

    def on_init(self, context):
        """Parse, gather, or set variables, settings, etc."""
        context['data_file'] = expand(self.vars['data_dir'] + '/cheatsheet.json')
        if not exists(context['data_file']):
            error(self.vim, f'Error accessing {context["data_file"]}')
            return

    def gather_candidates(self, context):
        """Fill a list with the candidates and send them onward."""
        candidates = []

        with open(context['data_file'], 'r') as fp:
            try:
                config = load(fp)
            except JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                error(self.vim, err_string)
                config = []

            for obj in config:
                candidates.append({
                    'word':            f"{obj['context']}  {obj['name']}  {obj['mapping']} {obj['command']}",
                    'action__command': obj['command'],
                    '__context':       obj['context'],
                    '__mapping':       obj['mapping'],
                    'abbr':            f"{obj['context']:<15}│{obj['name']:<20}│{obj['mapping']:<15}│:{obj['command']:<15}",

                })

        return candidates

    def _get_length(self, array, attribute):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_attr = item[attribute]
            cur_len = len(cur_attr)
            if cur_len > max_count:
                max_count = cur_len
        return max_count

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        # if self.vars['highlight_setting'] == 1:
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
                         f'containedin={self.syntax_name} contains={",".join(items)}')
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f'syntax match {self.syntax_name}_{pattern["name"]} {pattern["regex"]}')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        # if self.vars['highlight_setting'] == 1:
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    {'name': 'deniteSource_cheatsheet_Noise',     'link': 'Comment'     },
    {'name': 'deniteSource_cheatsheet_Context',   'link': 'Conditional' },
    {'name': 'deniteSource_cheatsheet_Command',   'link': 'Identifier'  },
    {'name': 'deniteSource_cheatsheet_Ctrl',      'link': 'Error'      },
    {'name': 'deniteSource_cheatsheet_Tab',       'link': 'Question'   },
    {'name': 'deniteSource_cheatsheet_Shift',     'link': 'Question'   },
    {'name': 'deniteSource_cheatsheet_Leader',    'link': 'Constant'   },
    {'name': 'deniteSource_cheatsheet_Title',     'link': 'Conditional'},
]

SYNTAX_PATTERNS = [
    # {'name': 'Noise',     'regex': r'/\(\s--\s\)/                        contained'},
    {'name': 'Noise',    'regex': r'/</                        contained'},
    {'name': 'Noise',    'regex': r'/>/                        contained'},
    {'name': 'Noise',    'regex': r'/│/  contained containedin=deniteSource_cheatsheet_Title'},
    {'name': 'Leader',   'regex': r'/leader/                   contained'},
    {'name': 'Leader',   'regex': r'/\v%(│)@<=(\[|\]|z|g)/     contained'},
    {'name': 'Leader',   'regex': r'/\v(i)(\w\s\/\sa\w)@=/     contained'},
    {'name': 'Leader',   'regex': r'/\v(i\w\s\/\s)@<=(a)/     contained'},
    {'name': 'Tab',      'regex': r'/Tab/                      contained'},
    {'name': 'Tab',      'regex': r'/\v%(S-)Tab/               contained'},
    {'name': 'Shift',    'regex': r'/S-\S/  contained contains=deniteSource_cheatsheet_Tab'},
    {'name': 'Ctrl',     'regex': r'/C-\S/                     contained'},
    {'name': 'Context',  'regex': r'/^\s\w\+/                  contained'},
    {'name': 'Command',  'regex': r'/:.\+/                     contained'},
    {'name': 'Title',    'regex': r'/\(CONTEXT\|│NAME\|│MAPPING\|│:COMMAND\)/ contained'},
    # {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained'},
    # {'name': 'Title',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    # {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
]
