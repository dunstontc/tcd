

""
" @setting(tcd#snippets_path)
" Full path to the folder containing Ultisnips snippets.
let g:tcd#snippets_path = '~/.dotfiles/editors/nvim/snipz'

" via http://vim.wikia.com/wiki/Capture_ex_command_output
" function! DataMessage(cmd) abort
"   redir => l:message
"   silent execute a:cmd
"   redir END
"   if empty(l:message)
"     echoerr 'no output'
"   else
"     " use "new" instead of "tabnew" below if you prefer split windows instead of tabs
"     new
"     setlocal buftype=nofile bufhidden=wipe noswapfile nobuflisted nomodified
"     silent put=l:message
"   endif
" endfunction

" command! -nargs=+ -complete=command DataMessage call DataMessage(<q-args>)



