" via http://vim.wikia.com/wiki/Capture_ex_command_output
function! DataMessage(cmd) abort
  redir => l:message
  silent execute a:cmd
  redir END
  if empty(l:message)
    echoerr 'no output'
  else
    " use "new" instead of "tabnew" below if you prefer split windows instead of tabs
    new
    setlocal buftype=nofile bufhidden=wipe noswapfile nobuflisted nomodified
    silent put=l:message
  endif
endfunction

command! -nargs=+ -complete=command DataMessage call DataMessage(<q-args>)

" function! OutputSplitWindow(...) abort
"   " this function output the result of the Ex command into a split scratch buffer
"   let cmd = join(a:000, ' ')
"   let temp_reg = @"
"   redir @"
"   silent! execute cmd
"   redir END
"   let output = copy(@")
"   let @" = temp_reg
"   if empty(output)
"     echoerr "no output"
"   else
"     new
"     setlocal buftype=nofile bufhidden=wipe noswapfile nobuflisted
"     put! =output
"   endif
" endfunction
" command! -nargs=+ -complete=command Output call OutputSplitWindow(<f-args>)
