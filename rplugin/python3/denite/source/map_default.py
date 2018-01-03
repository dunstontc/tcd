# ==============================================================================
#  FILE: mappings_default.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT license
#  Last Modified: 2017-12-24
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
        # self.syntax_name = 'deniteSource_Mappings'
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

