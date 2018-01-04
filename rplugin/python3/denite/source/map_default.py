# ==============================================================================
#  FILE: mappings_default.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT license
#  Last Modified: 2018-01-04
# ==============================================================================

# import re
import json

from .base import Base
# from ..kind.base import Base as BaseKind
# from denite import util


class Source(Base):

    def __init__(self, vim):

        super().__init__(vim)
        self.name         = 'map_default'
        self.kind         = 'command'
        self.syntax_name = 'deniteSource__Mapping'
        # self.sorters  = ['sorter_rank']
        # self.__re__tsv    = re.compile(r'^\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)')
        # self.__re_command = re.compile(r'^\|:.+\|')
        # self.__re_tokens  = re.compile(r'^\|:(.+)\|[\t\s]+:([^\t]+)[\t\s]+(.+)')
        # self.commands     = []
        self.vars = {
            'data_file': '/Users/clay/Projects/Vim/me/tcd/data/default_maps.json'
        }

    # def on_init(self, context):
        # raw_maps          = self.vim.call('execute', 'verbose nmap')

    def gather_candidates(self, context):
        candidates = []
        with open(self.vars['data_file']) as fp:
            # try:
                config = json.load(fp)
                for maps in config:
                    candidates.append({
                        'word': str(maps),
                        # 'abbr': maps['action'],
                        'abbr': '{0:^7} -- {1:^20} -- {2}'.format(maps['mode'], maps['char'], maps['action']),
                    })
                # candidate = sorted(candidate, key=itemgetter('source__command'))
            # except json.JSONDecodeError:
                # err_string = 'Decode error for' + self.vars['data_file']
                # util.error(self.vim, err_string)

        return candidates

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        # if self.vars['highlight_setting'] == 1:
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
                         f'containedin={self.syntax_name} contains={",".join(items)}')
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f'syntax match {self.syntax_name}_{pattern["name"]} {pattern["regex"]}')
            self.vim.command(r'syntax keyword deniteSource__Mapping_Notation contained	'
                             r'CR	NL	LF	BS	Tab	Esc	Space	')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        # if self.vars['highlight_setting'] == 1:
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    {'name': 'deniteSource__Mapping_Noise',     'link': 'Comment'     },
    {'name': 'deniteSource__Mapping_Insert',    'link': 'Identifier'  },
    {'name': 'deniteSource__Mapping_Normal',    'link': 'SpecialKey'  },
    {'name': 'deniteSource__Mapping_Visual',    'link': 'Conditional' },
    {'name': 'deniteSource__Mapping_Command',   'link': 'Type'        },
    {'name': 'deniteSource__Mapping_Notation',  'link': 'vimNotation' },
    {'name': 'deniteSource__Mapping_Ctrl',      'link': 'Error'       },
    {'name': 'deniteSource__Mapping_Motion',    'link': 'Type'        },
    {'name': 'deniteSource__Mapping_Shift',     'link': 'Question'    },
    {'name': 'deniteSource__Mapping_Leader',    'link': 'Constant'    },
    {'name': 'deniteSource__Mapping_Title',     'link': 'Conditional' },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',    'regex': r'/\(\s--\s\)/              contained'},
    {'name': 'Noise',    'regex': r'/</                        contained'},
    {'name': 'Noise',    'regex': r'/>/                        contained'},
    {'name': 'Notation', 'regex': r'/\s<\S\+>\s/                contained '
                                  r' contains=deniteSource__Mapping_Tab,deniteSource__Mapping_Shift,deniteSource__Mapping_Ctrl,deniteSource__Mapping_Noise'},
    {'name': 'Motion',   'regex': r'/{.\+}/                     contained'},
    {'name': 'Motion',   'regex': r'/`\S\+`/                     contained'},
    # {'name': 'Shift',    'regex': r'/S-\S/                     contained contains=deniteSource__Mapping_Tab'},
    # {'name': 'Ctrl',     'regex': r'/C-\S/                     contained'},
    {'name': 'Ctrl',     'regex': r'/C-\w+/                     contained'},
    {'name': 'Insert',   'regex': r'/^\s\+insert/              contained'},
    {'name': 'Normal',   'regex': r'/^\s\+normal/              contained'},
    {'name': 'Visual',   'regex': r'/^\s\+visual/              contained'},
    {'name': 'Command',  'regex': r'/^\s\+command/             contained'},
    # {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained'},
    # {'name': 'Title',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    # {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
]

# syn match	vimNotation	"\(\\\=<\|<lt>\)\([scamd]-\)\{0,4}x\=\(f\d\{1,2}\|[^ \t:]\|cr\|lf\|linefeed\|enter\|return\|k\=del\%[ete]\|bs\|backspace\|tab\|esc\|right\|left\|help\|undo\|insert\|ins\|k\=home\|k\=end\|kplus\|kminus\|kdivide\|kmultiply\|kenter\|kpoint\|space\|k\=\(page\)\=\(\|down\|up\|k\d\>\)\)>" contains=vimBracket
# syn match	vimNotation	"\(\\\=<\|<lt>\)\([scam2-4]-\)\{0,4}\(right\|left\|middle\)\(mouse\)\=\(drag\|release\)\=>"	contains=vimBracket



# def define_syntax(self):
#     self.vim.command('syntax case ignore')
#     self.vim.command(r'syntax match deniteSource_Mappings /\v^.*$/ containedin=' + self.syntax_name)
#     self.vim.command(r'syntax match deniteSource_MappingsBracket contained /<\S*>/ '
#                      r'contained containedin=deniteSource_Mappings')
#     # self.vim.command(r'syntax match deniteSource_MappingsMode /^\s\w\+/ contained '
#     self.vim.command(r'syntax match deniteSource_MappingsMode /\v^\s(command|insert|normal|visual)/')
#                      # r'contained containedin=deniteSource_Mappings')
#     # self.vim.command(r'syntax match deniteSource_MappingsLhs /\(^.*--\s\zs.*\ze--\)/ contained '
#                      # r'contained containedin=deniteSource_Mappings')
#     # self.vim.command(r'syntax match deniteSource_MappingsRhs /\v%(--.+--)\zs(.*$)\ze/ contained '
#                      # r'contained containedin=deniteSource_Mappings')
#
# def highlight(self):
#     self.vim.command('highlight default link deniteSource_Mappings Comment')
#     self.vim.command('highlight default link deniteSource_MappingsBracket Preprocessor')
#     self.vim.command('highlight default link deniteSource_MappingsMode Number')
#     self.vim.command('highlight default link deniteSource_MappingsRhs String')
#     # self.vim.command('highlight default link deniteSource_MappingsLhs Identifier')

# class Kind(BaseKind):
#     def __init__(self, vim):
#         super().__init__(vim)
#         self.default_action = 'execute'
#         self.name = 'mappingz'
#         self.persist_actions = []
#
#     def action_execute(self, context):
#         target = context['targets'][0]
#         command = target['source__command']
#         args = target['source__args']
#         if args:
#             util.clear_cmdline(self.vim)
#             self.vim.call('mappings#feedkeys', ':%s' % command)
#         else:
#             self.vim.call('denite#util#execute_command', command)
#

