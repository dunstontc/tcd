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
            'data_file': '/Users/clay/Projects/Vim/Denite/me/denite-mappings-source/default_maps.json'
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

    def highlight(self):
        """Link highlight groups to existing attributes."""
        # if self.vars['highlight_setting'] == 1:
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    # {'name': 'deniteSource_Projectile_Project',   'link': 'Normal'    },
    {'name': 'deniteSource_cheatsheet_Noise',     'link': 'Comment'    },
    {'name': 'deniteSource_cheatsheet_Context',   'link': 'Conditional'    },
    {'name': 'deniteSource_cheatsheet_Command',   'link': 'Identifier' },
    {'name': 'deniteSource_cheatsheet_Ctrl',      'link': 'Error'   },
    {'name': 'deniteSource_cheatsheet_Tab',       'link': 'Question'   },
    {'name': 'deniteSource_cheatsheet_Shift',     'link': 'Question'   },
    {'name': 'deniteSource_cheatsheet_Leader',    'link': 'Constant'   },
    {'name': 'deniteSource_cheatsheet_Title',     'link': 'Conditional'},
]

SYNTAX_PATTERNS = [
    # {'name': 'Noise',     'regex': r'/\(\s--\s\)/                        contained'},
    {'name': 'Noise',    'regex': r'/</                        contained'},
    {'name': 'Noise',    'regex': r'/>/                        contained'},
    {'name': 'Leader',   'regex': r'/leader/                   contained'},
    {'name': 'Tab',      'regex': r'/Tab/                      contained'},
    {'name': 'Tab',      'regex': r'/\v%(S-)Tab/               contained'},
    {'name': 'Shift',    'regex': r'/S-\S/                     contained contains=deniteSource_cheatsheet_Tab'},
    {'name': 'Ctrl',     'regex': r'/C-\S/                     contained'},
    {'name': 'Context',  'regex': r'/^\s\w\+/                   contained'},
    {'name': 'Command',  'regex': r'/:.\+/                     contained'},
    {'name': 'Title',    'regex': r'/\(context\|│name\|│mapping\|│:command\)/        contained'},
    # {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained'},
    # {'name': 'Title',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    # {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
]

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

