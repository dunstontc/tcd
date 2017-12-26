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
  - `:Denite var`
    - Source for Vim variables.


## Clean Cmdline Comp ##
  - **References**
    - [MarcWeber/vim-addon-commandline-completion](https://github.com/MarcWeber/vim-addon-commandline-completion/blob/master/autoload/cmdline_completion.vim)
  - **Steps**
    - `getcmdline()`
    - `redraw`
    - `<C-d>`
  - **Keys**
    - `:`
    - *...type...*
    - `<Plug>(hypertab-cmdline)`
      - `getcmdline()`
      - `<C-d>`
      - `<C-a>`
    - `getcmdline()`
      - `eescape(getcmdline(), ' \')`

## vim() ##
  - vim.buffers
  - vim.call(functionName, args)
    - vim.call(has, *var*)
    - vim.call(execute, *cmdline cmd*)
  - vim.command(command, args)
  - vim.eval(&var)
  - vim.options(option)
  - vim.vars.get(var)
  - vim.vvars['var']

