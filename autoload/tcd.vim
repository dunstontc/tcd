""
" @section Autoload, autoload
" Assorted functions.
"


""
" @function(tcd#ClearRegisters)
" Clear all registers.
" @via(https://github.com/wincent/wincent)
function! tcd#ClearRegisters() abort
  let l:regs='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-="*+'
  let l:i=0
  while (l:i<strlen(l:regs))
    exec 'let @'.l:regs[l:i].'=""'
    let l:i=l:i+1
  endwhile
endfunction

""
" function(tcd#SynStack)
" Log syntax scope(s) at the cursor.
" @via(https://github.com/mhartington/dotfiles/blob/master/config/nvim/init.vim#L217)
function! tcd#SynStack() abort
  if !exists('*synstack')
    return
  endif

  let l:syntaks = map(synstack(line('.'), col('.')), "synIDattr(v:val, 'name')")
  echo l:syntaks
endfunction

""
" @function(tcd#TwoSplit) {filepath}
" Given a {filepath}, either open or split the destination.
function! tcd#TwoSplit(filepath) abort
  " TODO: take non-string input. Parse $HOME.
  let l:confirmed = confirm('Open in a new window?', "&Yes\n&No", 2)
  if l:confirmed == 1
    execute "vsplit ".fnameescape(a:filepath)
  else
    execute "edit ".fnameescape(a:filepath)
  endif
endfunction

""
" @function(tcd#Demo)
" Prompts for a name and echos it back.
function! tcd#Demo()
  " let l:curline = getline('.')
  call inputsave()
  let l:name = input('Enter name: ')
  call inputrestore()
  " call setline('.', l:curline . ' ' . l:name)
  echo ' '
  echohl String
  echo 'Hello '.l:name.'!'
  echohl None
endfunction

" via http://vim.wikia.com/wiki/Capture_ex_command_output
" function! tcd#DataMessage(cmd) abort
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
"
" command! -nargs=+ -complete=command DataMessage call DataMessage(<q-args>)

" =============================================================================

" romainl/redir.vim
" function! tcd#Redir(cmd)
" 	for l:win in range(1, winnr('$'))
" 		if getwinvar(l:win, 'scratch')
" 			execute l:win . 'windo close'
" 		endif
" 	endfor
" 	if a:cmd =~ '^!'
" 		execute "let output = system('" . substitute(a:cmd, '^!', '', '') . "')"
" 	else
" 		redir => output
" 		execute a:cmd
" 		redir END
" 	endif
" 	vnew
" 	let w:scratch = 1
" 	setlocal nobuflisted buftype=nofile bufhidden=wipe noswapfile
" 	call setline(1, split(output, "\n"))
" endfunction
"
" command! -nargs=1 Redir silent call Redir(<f-args>)

" Usage:
" 	:Redir hi ............. show the full output of command ':hi' in a scratch window
" 	:Redir !ls -al ........ show the full output of command ':!ls -al' in a scratch window



" =============================================================================
""
" @private
"
function! s:fnameescape(file) abort
  if exists('*fnameescape')
    return fnameescape(a:file)
  else
    return escape(a:file," \t\n*?[{`$\\%#'\"|!<")
  endif
endfunction

function! s:runtime_globpath(file) abort
  return split(globpath(escape(&runtimepath, ' '), a:file), "\n")
endfunction

