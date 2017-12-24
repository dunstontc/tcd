"""Let's interact with Ultisnips."""
# ============================================================================
# FILE:    ultisnips.py
# AUTHOR:  Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# source:  https://github.com/neoclide/ultisnips/blob/master/rplugin/python3/denite/source/ultisnips.py
# ============================================================================

# import os
# from operator import itemgetter

# from ..kind.file import Kind as File
from .base import Base


def get_width(array, attribute):
    """Get the max string length for an attribute in a collection."""
    max_count = int(0)
    for item in array:
        cur_attr = item[attribute]
        cur_len = len(cur_attr)
        if cur_len > max_count:
            max_count = cur_len
    return max_count


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'ultisnips'
        self.matchers = ['matcher_regexp']
        self.kind = 'word'
        self.vars = {
            'snippets_dirs': vim.vars.get('UltiSnipsSnippetDirectories'),
            'snippets_dir': vim.vars.get('UltiSnipsSnippetsDir'),
        }

    def on_init(self, context):
        # if self.vars['snippets_dirs']
        context['snippetz'] = self.vim.call('tcd#GetAllSnippets')
        # noop = int(0)
        # key_len = noop
        # for item in context['snippetz']:
        #     if len(item['key']) > key_len:
        #         key_len = len(item['key'])


    def gather_candidates(self, context):
        candidates = []
        key_len = get_width(context['snippetz'], 'key')

        for item in context['snippetz']:
            candidates.append({
                'word': item['key'],
                'abbr': f"{item['key']:<{key_len}} -- {item['description']}",
                '__path': item['path'],
                '__line': item['linenr']
            })
        return candidates

# {
#     'linenr': '692',
#     'description': 'triple quoted string (double quotes)',
#     'key': '"',
#     'path': '/Users/clay/.dotfiles/editors/nvim/snipz/python.snippets'
# }
# class Kind(File):
#     """
#     Kind of ultisnips source
#     """
#     def __init__(self, vim):
#         super().__init__(vim)
#
#         self.default_action = 'expand'
#         self.name = 'todo'
#         self.sorters = []
#
#     def action_expand(self, context):
#         """
#         expand snippet
#         """
#         target = context['targets'][0]
#         command = target['source__command']
#         trigger = target['source__trigger']
#         self.vim.command('normal %sa%s ' % (command, trigger))
#         self.vim.call('UltiSnips#ExpandSnippet')
#
#     def action_edit(self, context):
#         """
#         edit snippet
#         """
#         return self.action_open(context)


    # def gather_candidates(self, context):
    #     args = dict(enumerate(context['args']))
    #     is_all = str(args.get(0, '')) == 'all'
    #     if is_all:
    #         items = self.vim.call('UltiSnips#SnippetsInCurrentScope', 1)
    #     else:
    #         items = self.vim.call('UltiSnips#SnippetsInCurrentScope', 0)
    #
    #     items = sorted(items, key=itemgetter('priority', 'filepath'), reverse=True)
    #     candidates = []
    #     for item in items:
    #         locs = item['location'].split(':')
    #         base = os.path.basename(locs[0])
    #         fname = os.path.splitext(base)[0]
    #         candidates.append({
    #             'word': '%s %s' % (item['key'], item['description']),
    #             'abbr': '%-12s%-20s     %s' % (fname, item['key'], item['description']),
    #             'action__path': locs[0],
    #             'action__line': locs[1],
    #             'action__col': 0,
    #             'source__command': context['__command'],
    #             'source__trigger': item['key'],
    #             })
    #     return candidates

    # def highlight(self):
    #     self.vim.command(r'highlight default link deniteSource__UltisnipsPath        Comment')
    #     self.vim.command(r'highlight default link deniteSource__UltisnipsTrigger     Identifier')
    #     self.vim.command(r'highlight default link deniteSource__UltisnipsDescription Statement')
    #
    # def define_syntax(self):
    #     self.vim.command('syntax case ignore')
    #     self.vim.command(r'syntax match deniteSource__UltisnipsHeader /^.*$/ '
    #                      r'containedin=' + self.syntax_name)
    #     self.vim.command(r'syntax match deniteSource__UltisnipsPath        /\v^\s.{-}\ze\s/ contained '
    #                      r'containedin=deniteSource__UltisnipsHeader')
    #     self.vim.command(r'syntax match deniteSource__UltisnipsTrigger     /\%14c.*\%38c/ contained '
    #                      r'containedin=deniteSource__UltisnipsHeader')
    #     self.vim.command(r'syntax match deniteSource__UltisnipsDescription /\%39c.*$/ contained '
    #                      r'containedin=deniteSource__UltisnipsHeader')

# # ==============================================================================
# #  FILE: ultisnips.py
# #  AUTHORS: Alex LaFroscia & Herrington Darkholme
# #  License: GPL v3.0
# #  Last Modified: Jan 22, 2016
# # ==============================================================================
#
# from .base import Base
#
# class Source(Base):
#     def __init__(self, vim):
#         Base.__init__(self, vim)
#
#         self.name = 'ultisnips'
#         self.mark = '[US]'
#         self.rank = 8
#
#     def gather_candidates(self, context):
#         suggestions = []
#         snippets = self.vim.eval(
#             'UltiSnips#SnippetsInCurrentScope()')
#         for trigger in snippets:
#             suggestions.append({
#                 'word': trigger,
#                 'menu': self.mark + ' ' + snippets.get(trigger, ''),
#                 'dup': 1
#             })
#         return suggestions
#
