"""A Denite source for :messages."""
# ==============================================================================
#  FILE: messages.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
# ==============================================================================

import os
from os.path import join
import glob
import importlib.machinery


from .base import Base
from denite import util


class Source(Base):
    """Make it easier to see our messages."""

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'messages'
        self.kind = 'word'
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'snippets_dir': vim.vars.get('UltiSnipsSnippetDirectories'),
            'rtp': vim.vars.get('&rtp'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
            'has_devicons': vim.vars.get('loaded_devicons'),
        }

    def on_init(self, context):
        context['__messages'] = self.vim.call('messages').split('\n')


    def gather_candidates(self, context):
        # the_rtp = self.vim.options['runtimepath'].split(',')
        # cmd = f"find {' '.join({the_rtp})} -type f | egrep \"(?:.*/rplugin/python3/denite/source/*)(\w*\.py)\""


        candidates = []
        # for item in context.get('source', ''):
        with open('/Users/clay/test/runtimepath.txt', 'w') as the_file:
            for item in self.vim.options['runtimepath'].split(','):
                the_file.write(item + '\n')
                candidates.append({
                    'word': 'test',
                    'abbr': ' '.join(item.values()[1])
                    # 'abbr': str(item.values())
                })
        return candidates

    def find_rplugins(context, source, loaded_paths):
        """Search for *.py (From util.py)

        Searches $VIMRUNTIME/*/rplugin/python3/denite/$source/

        """
        # TODO: jackpot

        src = join('rplugin/python3/denite', source, '*.py')
        for runtime in context.get('runtimepath', '').split(','):
            for path in glob.iglob(os.path.join(runtime, src)):
                name = os.path.splitext(os.path.basename(path))[0]
                if ((source != 'kind' and name == 'base') or
                        name == '__init__' or path in loaded_paths):
                    continue
                yield path, name

    def load_sources(self, context):
        """Load sources from runtimepath.
            (From denite.py)
        """

        loaded_paths = [x.path for x in self._sources.values()]
        for path, name in self.find_rplugins(context, 'source', loaded_paths):
            module = importlib.machinery.SourceFileLoader(
                'denite.source.' + name, path).load_module()
            source = module.Source(self._vim)
            self._sources[source.name] = source
            source.path = path
            syntax_name = 'deniteSource_' + source.name.replace('/', '_')
            if not source.syntax_name:
                source.syntax_name = syntax_name

            if source.name in self._custom['alias_source']:
                # Load alias
                for alias in self._custom['alias_source'][source.name]:
                    self._sources[alias] = module.Source(self._vim)
                    self._sources[alias].name = alias
                    self._sources[alias].path = path
                    self._sources[alias].syntax_name = syntax_name
