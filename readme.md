# T.C.D. #

These are scripts, functions, and ideas that I'm fooling around with; feel free to have a look.

## Denite Sources ##
  - `:Denite env`
    - Source for environment variables. 
    - *(ex: $HOME)*
  - `:Denite rtp`
    - Source for Vim's runtime path.
  - `:Denite messages`
    - Source for Vim's messages.
  - `:Denite sauce`
    - Source for Denite sources.
    - *(ex: :Denite sauce)*
  - `:Denite sauce_file`
    - Source for Denite source files. 
    - *(ex: sauce_file.py)*
  - `:Denite syntax`
    - Source for Vim's syntax.
  - `:Denite ultisnips`
    - Source for Ultisnips snippets.
  - `:Denite ultisnips_files`
    - Source for Ultisnips snippet files.
  - `:Denite var`
    - Source for Vim variables.


## vim api ##
  - vim.buffers
  - vim.call(functionName, args)
    - vim.call(has, *var*)
    - vim.call(execute, *cmdline cmd*)
  - vim.command(command, args)
  - vim.eval(&var)
  - vim.options(option)
  - vim.vars.get(var)
  - vim.vvars['var']

