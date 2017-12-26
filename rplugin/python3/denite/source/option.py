"""A Denite source for Vim options."""
# ==============================================================================
#  FILE: option.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-24
# ==============================================================================

from re import compile, search

from .base import Base


class Source(Base):
    """Make it easier to see our options."""

    def __init__(self, vim):
        """Character creation."""
        super().__init__(vim)

        self.name = 'option'
        self.kind = 'word'
        self.vars = {}

    def on_init(self, context):
        """Capture variables."""
        context['__options'] = self.vim.call('execute', 'let ').split('\n')

    def gather_candidates(self, context):
        """And send the vars onward."""
        search_pattern = compile(r'^(\S+)\s+(.*)$', re.M)
        candidates = []
        for item in context['__options']:
            candidates.insert(0, {
                # 'word': 'test',
                'word': item
                # 'abbr': str(item.values())
                # join(item.values()[1])
            })
        # return self._convert(candidates)
            matches = search_pattern.search(item)
            if matches:
                candidates.append({
                    'word': matches.group(1),
                    '__description': matches.group(2)
                })
        return candidates

    def _convert(self, candidates):
        """Format and add metadata to gathered candidates.

        Parameters
        ----------
        candidates : list

        Returns
        -------
        A sexy source.

        """
        # option_len = self._get_length(candidates, 'option')
        # value_len  = self._get_length(candidates, 'value')

        for candidate in candidates:
            candidate['abbr'] = "{0:^{option_len}} -- {1:<{value_len}}".format(
                candidate['option'],
                candidate['value'],
            )
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

    # def define_syntax(self):
    #     self.vim.command(r'syntax match deniteSource_Messages /^.*$/ containedin=' + self.syntax_name + ' '
    #                      r'contains=deniteSource_Messages_Origin,deniteSource_Messages_String,deniteSource_Messages_Command,deniteSource_Messages_Err')
    #     self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s(.*)\s/   contained ')
    #     self.vim.command(r'syntax match deniteSource_Messages_Origin   /^\s\[.*\]\s/ contained ')
    #     self.vim.command(r'syntax match deniteSource_Messages_String   /\s".*"/      contained ')
    #     self.vim.command(r"syntax match deniteSource_Messages_String   /\s'.*'/      contained ")
    #     self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*\s\ze/ contained ')
    #     self.vim.command(r'syntax match deniteSource_Messages_Command  /\s:\w*$/     contained ')
    #     self.vim.command(r'syntax match deniteSource_Messages_Err      /\[DEW]\d\{3\}\%(:\)/   contained ')
    #
    # def highlight(self):
    #     self.vim.command('highlight default link deniteSource_Messages         Normal')
    #     self.vim.command('highlight default link deniteSource_Messages_Origin  Type')
    #     self.vim.command('highlight default link deniteSource_Messages_String  String')
    #     self.vim.command('highlight default link deniteSource_Messages_Command PreProc')
    #     self.vim.command('highlight default link deniteSource_Messages_Err     Error')
