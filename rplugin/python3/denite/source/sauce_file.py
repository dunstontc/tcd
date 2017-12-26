"""A Denite source for Denite sources."""
# ==============================================================================
#  FILE:          sauce.py
#  AUTHOR:        Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-26
# ==============================================================================

from os.path import splitext, basename

from .base import Base
from denite import util


class Source(Base):
    """I wanna be the very best, like no one ever was."""

    def __init__(self, vim):
        """To catch them is my real test, to train them is my cause."""
        super().__init__(vim)

        self.name = 'sauce_file'
        self.kind = 'file'
        self.vars = {}

    def on_init(self, context):
        """I will travel across the land, searching far and wide.

        TODO: Actions just feed the word, but if there are arg options, prompt for them.

        """
        context['__sauces'] = self.vim.call('tcd#GetCommandCompletion', 'Denite ')

    def gather_candidates(self, context):
        """Each Denite source, to understand, the power that's insiiide."""
        candidates = []

        # for sauce in context['__sauces']:
        #     candidates.append({
        #         'word': sauce,
        #         # 'word': ', '.join(teest),
        #     })
        for file in util.globruntime(context['runtimepath'], 'rplugin/python3/denite/source/*.py'):
            source = splitext(basename(file))[0]
            root = util.path2project(self.vim, file, '.git')
            if source != str('__init__') and source != str('base'):
                candidates.append({
                    'word': source,
                    'abbr': f"{source} -- {root}",
                    'action__command': 'Denite ' + source,
                    'action__path': str(file),
                    '__source_name': source
                })

        # return sorted(sources.values(), key=lambda value: value['word'])
        return candidates

    # def load_sources(self, context):
    #     """Load sources from runtimepath.
    #
    #     (From denite.py)
    #     """
    #     loaded_paths = [x.path for x in self._sources.values()]
    #     for path, name in self.find_rplugins(context, 'source', loaded_paths):
    #         module = importlib.machinery.SourceFileLoader(
    #             'denite.source.' + name, path).load_module()
    #         source = module.Source(self._vim)
    #         self._sources[source.name] = source
    #         source.path = path
    #         syntax_name = 'deniteSource_' + source.name.replace('/', '_')
    #         if not source.syntax_name:
    #             source.syntax_name = syntax_name
    #
    #         if source.name in self._custom['alias_source']:
    #             # Load alias
    #             for alias in self._custom['alias_source'][source.name]:
    #                 self._sources[alias] = module.Source(self._vim)
    #                 self._sources[alias].name = alias
    #                 self._sources[alias].path = path
    #                 self._sources[alias].syntax_name = syntax_name
