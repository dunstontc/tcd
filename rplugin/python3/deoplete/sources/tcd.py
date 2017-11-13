import os
from .base import Base


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        """
            Every source requires a name.
        """
        self.name = 'tcd'
        """
            This is what shows up next to the item in the completion menu,
            you should probably keep this short
        """
        self.mark = '[tcd]'
        """
            This is how many characters need to be typed before completion pops up.
            Since snippets are short by nature, I remove the need altogether.
            The default is 2 which is too long for my snippets which are things such as if, vd etc...
        """
        self.min_pattern_length = 0
        """
            This is the minisnip_directory set by minisnip.
            If none is entered in your vimrc, it looks in ~/.vim/minisnip.
            Note the use of self.vim.eval
            this basically calls vim and returns the result.
        """
        self.tcd = self.vim.eval('g:tcd')
        """
            This is a list of all the snippets in our self.minisnip_dir.
        """
        self.snippets = os.listdir(self.tcd)

    def gather_candidates(self, context):
        return ['hello from Python!']
