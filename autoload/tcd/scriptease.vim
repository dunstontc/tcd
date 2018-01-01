" ""
" " These functions were taken directly from @tpope/scriptease. Link below.
" " https://github.com/tpope/vim-scriptease/blob/master/autoload/scriptease.vim
"
" let s:escapes = {
"       \ "\b": '\b',
"       \ "\e": '\e',
"       \ "\f": '\f',
"       \ "\n": '\n',
"       \ "\r": '\r',
"       \ "\t": '\t',
"       \ "\"": '\"',
"       \ "\\": '\\'}
"
"
" ""
" " @function(tcd#scriptease#dump) {object}, [...]
" "
" function! tcd#scriptease#dump(object, ...) abort
"   let opt = extend({'width': 0, 'level': 0, 'indent': 1, 'tail': 0, 'seen': []}, a:0 ? copy(a:1) : {})
"   let opt.seen = copy(opt.seen)
"   let childopt = copy(opt)
"   let childopt.tail += 1
"   let childopt.level += 1
"   for i in range(len(opt.seen))
"     if a:object is opt.seen[i]
"       return type(a:object) == type([]) ? '[...]' : '{...}'
"     endif
"   endfor
"   if type(a:object) ==# type('')
"     if a:object =~# "[\001-\037']"
"       let dump = '"'.s:gsub(a:object, "[\001-\037\"\\\\]", '\=get(s:escapes, submatch(0), printf("\\%03o", char2nr(submatch(0))))').'"'
"     else
"       let dump = string(a:object)
"     endif
"   elseif type(a:object) ==# type([])
"     let childopt.seen += [a:object]
"     let dump = '['.join(map(copy(a:object), 'tcd#scriptease#dump(v:val, {"seen": childopt.seen, "level": childopt.level})'), ', ').']'
"     if opt.width && opt.level + len(s:gsub(dump, '.', '.')) > opt.width
"       let space = repeat(' ', opt.level)
"       let dump = "[".join(map(copy(a:object), 'tcd#scriptease#dump(v:val, childopt)'), ",\n ".space).']'
"     endif
"   elseif type(a:object) ==# type({})
"     let childopt.seen += [a:object]
"     let keys = sort(keys(a:object))
"     let dump = '{'.join(map(copy(keys), 'tcd#scriptease#dump(v:val) . ": " . tcd#scriptease#dump(a:object[v:val], {"seen": childopt.seen, "level": childopt.level})'), ', ').'}'
"     if opt.width && opt.level + len(s:gsub(dump, '.', '.')) > opt.width
"       let space = repeat(' ', opt.level)
"       let lines = []
"       let last = get(keys, -1, '')
"       for k in keys
"         let prefix = scriptease#dump(k) . ':'
"         let suffix = scriptease#dump(a:object[k]) . ','
"         if len(space . prefix . ' ' . suffix) >= opt.width - (k ==# last ? opt.tail : '')
"           call extend(lines, [prefix, scriptease#dump(a:object[k], childopt) . ','])
"         else
"           call extend(lines, [prefix . ' ' . suffix])
"         endif
"       endfor
"       let dump = s:sub("{".join(lines, "\n " . space), ',$', '}')
"     endif
"   elseif type(a:object) ==# type(function('tr'))
"     let dump = s:sub(s:sub(string(a:object), '^function\(''(\d+)''', 'function(''{\1}'''), ',.*\)$', ')')
"   else
"     let dump = string(a:object)
"   endif
"   return dump
" endfunction
"
" ""
" " @function(tcd#scriptease#filterop) {object}, [...]
" "
" function! tcd#scriptease#filterop(type) abort
"   let reg_save = @@
"   try
"     let expr = s:opfunc(a:type)
"     let @@ = matchstr(expr, '^\_s\+').tcd#scriptease#dump(eval(s:gsub(expr,'\n%(\s*\\)=',''))).matchstr(expr, '\_s\+$')
"     if @@ !~# '^\n*$'
"       normal! gvp
"     endif
"   catch /^.*/
"     echohl ErrorMSG
"     echo v:errmsg
"     echohl NONE
"   finally
"     let @@ = reg_save
"   endtry
" endfunction
"
" nnoremap <silent> <Plug>ScripteaseFilter :<C-U>set opfunc=tcd#scriptease#filterop<CR>g@
" xnoremap <silent> <Plug>ScripteaseFilter :<C-U>call tcd#scriptease#filterop(visualmode())<CR>
" if empty(mapcheck('g!', 'n'))
"   nmap g! <Plug>ScripteaseFilter
"   nmap g!! <Plug>ScripteaseFilter_
" endif
" if empty(mapcheck('g!', 'x'))
"   xmap g! <Plug>ScripteaseFilter
" endif
"
"
" ""
" " @subsection Private, private
" "
"
" ""
" " @private
" " @function(s:opfunc({type}))
" function! s:opfunc(type) abort
"   let sel_save = &selection
"   let cb_save = &clipboard
"   let reg_save = @@
"   try
"     set selection=inclusive clipboard-=unnamed clipboard-=unnamedplus
"     if a:type =~ '^\d\+$'
"       silent exe 'normal! ^v'.a:type.'$hy'
"     elseif a:type =~# '^.$'
"       silent exe "normal! `<" . a:type . "`>y"
"     elseif a:type ==# 'line'
"       silent exe "normal! '[V']y"
"     elseif a:type ==# 'block'
"       silent exe "normal! `[\<C-V>`]y"
"     else
"       silent exe "normal! `[v`]y"
"     endif
"     redraw
"     return @@
"   finally
"     let @@ = reg_save
"     let &selection = sel_save
"     let &clipboard = cb_save
"   endtry
" endfunction
"
" ""
" " @private
" " @function(s:sub) {str}, {pat}, {rep}
" "
" function! s:sub(str,pat,rep) abort
"   return substitute(a:str,'\v\C'.a:pat,a:rep,'')
" endfunction
"
" ""
" " @private
" " @function(s:gsub) {str}, {pat}, {rep}
" "
" function! s:gsub(str,pat,rep) abort
"   return substitute(a:str,'\v\C'.a:pat,a:rep,'g')
" endfunction
