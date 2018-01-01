# noqa: D100
# ==============================================================================
#  FILE: test.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
# ==============================================================================


import arrow
import os

# from denite.util import clear_cmdline

from .base import Base
from ..kind.base import Base as BaseKind


time = arrow.utcnow().format('MM_DD-HH.mm.ss')
filename = f'/Users/clay/test/denite_tests/{time}.txt'


class Source(Base):  # noqa: D101

    def __init__(self, vim):  # noqa: D107
        super().__init__(vim)
        self.name = 'test'
        self.kind = Kind(vim)
        self.vars = {}

    def on_init(self, context): # noqa
        context['__linenr']   = self.vim.current.window.cursor[0]
        context['__bufname']  = self.vim.current.buffer.name
        context['__bufnr']    = self.vim.current.buffer.number
        context['__filename'] = os.path.basename(context['__bufname'])

        context['__eval']     = self.vim.call('eval', '&rtp ').split(',')
        context['__execute']  = self.vim.call('getqflist')
        # exe = self.vim.call('getqflist')
        # context['__command'] = self.vim.call('execute', 'script').split('\n')

        # with open('/Users/clay/test/denite_tests/source_context.txt', 'w+') as filet:
        #     # filet.writelines(exe)
        #     for item in context:
        #         filet.write("{}\n".format(item))

    def gather_candidates(self, context):  # noqa: D102
        candidates = [({ 'word': 'Remain calm, this is only a test -- 1' })]
        candidates += [({ 'word': 'Remain calm, this is only a test -- 2' })]
        candidates += [({ 'word': 'Remain calm, this is only a test -- 3' })]

        context['all_the_candy'] = candidates
        # with open('/Users/clay/test/denite_tests/source_context.txt', 'w+') as filet:
            # filet.write(str(context))
            # for item in context:
                # filet.write("{}\n".format(item))

        return candidates


class Kind(BaseKind):  # noqa: D101

    def __init__(self, vim):  # noqa: D107
        super().__init__(vim)
        self.default_action = 'test'
        self.name = 'todo'
        self.persist_actions = []

    def action_test(self, context):  # noqa: D102
        # target = context['targets'][0]
        with open('/Users/clay/test/denite_tests/kind_context.txt', 'w+') as filet:
            filet.write(str(context))
            # for item in context:
            # filet.write("{}\n".format(item))
        return

    def action_append(self, context):  # noqa: D102
        target = context['targets'][0]
        new_items = []

        for x in 10:
            new_items.append({
                'bufnr': 2,     # Buffer Number
                'col':  target['action__col'],   # Column Number
                'lnum': target['action__line'],  # Line Number
                'nr': -1,       # ???
                'pattern': '',  # ???
                'text': target['content'],       # Content
                'type': 'W',    # Type
                'valid': 1,                      # Yes
                'vcol': 0                        # Virtual Column
            })

    def get_loclist(self, context):
        winnr = self.vim.eval('bufwinnr("' + context['__bufname'] + '")')
        items = self.vim.eval('getloclist(' + str(winnr) + ')')
        res = []
        for item in items:
            if item['valid'] != 0:
                res.append(self.convert(item, context))
        return res




