
""
" @section Functions, functions
" Assorted functions.
"

""
" @public
" @function(tcd#ClearRegisters)
" Clear all registers.
" via(https://github.com/wincent/wincent)
function! tcd#ClearRegisters() abort
  let l:regs='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-="*+'
  let l:i=0
  while (l:i<strlen(l:regs))
    exec 'let @'.l:regs[l:i].'=""'
    let l:i=l:i+1
  endwhile
endfunction

""
" @public
" function(tcd#SynStack)
" Log syntax scope(s) at the cursor.
" via(https://github.com/mhartington/dotfiles/blob/master/config/nvim/init.vim#L217)
function! tcd#SynStack() abort
  if !exists('*synstack')
    return
  endif

  let l:syntaks = map(synstack(line('.'), col('.')), "synIDattr(v:val, 'name')")
  echo l:syntaks
endfunction

""
" @public
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
" @public
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

""
" @public
" @function(mappings#feedkeys) {keys}
" From chemzqm/denite-extras
function! tcd#Feedkeys(keys)
  let s:map = a:keys
  " let s:map = substitute(s:map, '<NL>', '<C-j>', 'g')
  " let s:map = substitute(s:map, '\(<.*>\)', '\\\1', 'g')
  if !exists('*timer_start')
    echohl Error | echon 'timer_start requires for feedkeys to work' | echohl None
  else
    function! s:Callback(...)
      " call feedkeys(s:map .'', 't')
        execute(s:map)
      " call feedkeys("\<CR>", 'm')
    endfunction
    call timer_start(500, function('s:Callback'))
  endif
endfunction

""
" @public
" @function(mappings#search) {keys}
" From chemzqm/denite-extras
function! tcd#Search(keys)
  let l:keys = a:keys
  function! Callback(...)
    call feedkeys('/' . l:keys . "\<CR>", 't')
  endfunction
  call timer_start(100, function('Callback'))
endfunction


""
" Returns a list with all Ultisnips snippets in the current scope.
function! tcd#GetAllSnippets()
  call UltiSnips#SnippetsInCurrentScope(1)
  let l:list = []
  for [l:key, l:info] in items(g:current_ulti_dict_info)
    let l:parts = split(l:info.location, ':')
    call add(l:list, {
      \'key': l:key,
      \'path': l:parts[0],
      \'linenr': l:parts[1],
      \'description': l:info.description,
      \})
  endfor
  return l:list
endfunction


""
" @subsection Private Functions
"

""
" @private
" @function(s:escape) {filepath}
function! s:escape(filepath)
  return "'".substitute(a:filepath, "'", "\\'", 'g')."'"
endfunction

""
" @private
" @function(s:fnameescape) {file}
function! s:fnameescape(file) abort
  if exists('*fnameescape')
    return fnameescape(a:file)
  else
    return escape(a:file," \t\n*?[{`$\\%#'\"|!<")
  endif
endfunction

""
" @private
" @function(s:runtime_globpath) {file}
function! s:runtime_globpath(file) abort
  return split(globpath(escape(&runtimepath, ' '), a:file), "\n")
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

