""
" @section Functions, functions
" Assorted functions.
"

""
" @public
" Clear all registers.
" From 'https://github.com/wincent/wincent'
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
" Log syntax scope(s) at the cursor.
" From https://github.com/mhartington/dotfiles/blob/master/config/nvim/init.vim#L217'
function! tcd#SynStack() abort
  if !exists('*synstack')
    return
  endif

  let l:syntaks = map(synstack(line('.'), col('.')), "synIDattr(v:val, 'name')")
  echo l:syntaks
endfunction

""
" @public
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
" Prompts for a name and echos it back.
function! tcd#Demo()
  call inputsave()
  let l:name = input('Enter name: ')
  call inputrestore()
  echo ' '
  echohl String
  echo 'Hello '.l:name.'!'
  echohl None
endfunction

""
" @public
" From 'https://github.com/chemzqm/denite-extras'
function! tcd#Chemzqm_Feedkeys(keys)
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
" From 'https://github.com/chemzqm/denite-extras'
function! tcd#Chemzqm_Search(keys)
  let l:keys = a:keys
  function! Callback(...)
    call feedkeys('/' . l:keys . "\<CR>", 't')
  endfunction
  call timer_start(100, function('Callback'))
endfunction

""
" @public
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
" @public
" Capture wildmode completion options for `:echo $ <Tab>`
" From 'https://stackoverflow.com/questions/11175842/how-to-list-all-the-environment-variables-in-vim'
" '<c-a>' Inserts all possible completion options.
function! tcd#Env() abort
    redir => l:s
    sil! exe "norm!:ec$\<c-a>'\<c-b>\<right>\<right>\<del>'\<cr>"
    redir END
    return split(l:s)
endfunction

""
" @public
" (see :help |denite|)
function! tcd#GetChar() abort
  redraw | echo 'Press any key: '
  let l:c = getchar()
  while l:c ==# "\<CursorHold>"
    redraw | echo 'Press any key: '
    let l:c = getchar()
  endwhile
  redraw | echomsg printf('Raw: "%s" | Char: "%s"', l:c, nr2char(l:c))
endfunction
command! GetChar call s:getchar()

""
" @public
" From 'https://stackoverflow.com/questions/21117615/how-to-obtain-command-completion-list'
function! tcd#GetCommandCompletion( base )
    silent execute "normal! :" a:base . "\<C-a>')\<C-b>return split('\<CR>"
endfunction

" ""
" " @public
" " Get cmdline completion suggestions and redraw.
" " NOTE: wip
" function! tcd#SexySuggest()
"   let l:current_text = getcmdline()
"   let l:current_pos  = getcmdpos()
"   let l:suggestions  = tcd#GetCommandCompletion(l:current_text)
"   silent execute "normal! :" l:suggestions . "\<C-a>')\<C-b>return split('\<CR>"
" endfunction

" ""
" " @public
" " Redraw and get cmdline completion suggestions.
" " NOTE: wip
" function! tcd#Redraw() abort
"   let l:current_text = getcmdline()
"   " call feedkeys("\<C-c>") | echo '' | call feedkeys( ':' . l:current_text . "\<C-d>" )
"   " redraw | echo '' | call feedkeys("\<C-d>")
"   " silent! redraw
"   let s:map = getcmdline()
"   " let s:map = substitute(s:map, '<NL>', '<C-j>', 'g')
"   " let s:map = substitute(s:map, '\(<.*>\)', '\\\1', 'g')
"   function! s:Callback(...)
"     call feedkeys(s:map ."\<C-D>", 't')
"       execute(s:map)
"     " call feedkeys("\<CR>", 'm')
"   endfunction
"   echo ' '
"   call timer_start(500, function('s:Callback'))
" endfunction

" ""
" " @public
" " Get cmdline completion suggestions and redraw.
" " NOTE: wip
" function! tcd#Redraw() abort
"   let l:current_text = getcmdline()
"   redraw | call feedkeys(':' . l:current_text . "\<C-d>")
" endfunction

" ""
" " @function(tcd#ReReg)
" " Replace register {from} with the contents of register {to}
" function! tcd#ReReg(from, to) abort
"   let l:keep = a:from
"   let l:junk = a:to
"   let l:keeping = '@'.a:from.''
"   let l:junked = '@'.a:to.''
"   silent execute "let @".l:junk." = @".l:keep
"   execute "echo ".l:junked." ".l:keeping.""
" endfunction

""
" @function(tcd#NewID)
" Used to increment ids for todo.txt files.
" Returns the highest id in a buffer +1.
function! tcd#NewID() abort
  let l:cur_val = 0
  " let l:new_val = 0
  " let l:cur_id = 'id:'.l:cur_val.''
  let l:match = search('id:'.l:cur_val.'', 'nw')
  if l:match != 0
    let l:curval += 1
  else
    return l:cur_val
  endif
  " while search('id:'.l:cur_val.'', 'nw') != 0
    " let l:cur_val += 1
    " let l:new_val += 1
  " endwhile
  " echo l:cur_val
endfunction

function! tcd#Count( word )
  redir => cnt
    silent exe '%s/' . a:word . '//gn'
  redir END

  let res = strpart(cnt, 0, stridx(cnt, " "))
  return res
endfunction


""
" @function(s:get_register)
" From `hecal3/vim-leader-guide`
function! tcd#get_register()
    if match(&clipboard, 'unnamedplus') >= 0
        let g:tcd#clip = '+'
    elseif match(&clipboard, 'unnamed') >= 0
        let g:tcd#clip = '*'
    else
        let g:tcd#clip = '"'
    endif
    return clip
endfunction

""
" @public
" tcd#JumpInFile({back}, {forw})
" https://stackoverflow.com/questions/7066456/vim-how-to-prevent-jumps-out-of-current-buffer
function! tcd#JumpInFile(back, forw)
    let [n, i] = [bufnr('%'), 1]
    let p = [n] + getpos('.')[1:]
    sil! exe 'norm!1' . a:forw
    while 1
        let p1 = [bufnr('%')] + getpos('.')[1:]
        if n == p1[0] | break | endif
        if p == p1
            sil! exe 'norm!' . (i-1) . a:back
            break
        endif
        let [p, i] = [p1, i+1]
        sil! exe 'norm!1' . a:forw
    endwhile
endfunction


" function Find()
"     execute "g!/Script/d"
"     execute "sort"
"     normal G
"     normal 0v$"ay
"     normal u
"     execute "call search('".@a."')"
"   endfunction

""
" @subsection Private Functions
" Assorted helper functions not in the global scope.
" ==============================================================================


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

