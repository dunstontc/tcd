""
" Function from romainl/vim-qf.
" Allows commands like `:lnext` and `:lprev` to wrap around a file.
" link: https://github.com/romainl/vim-qf/blob/master/autoload/qf/wrap.vim
" see also: https://stackoverflow.com/a/27204000/7687024
function! tcd#qf#WrapCommand(direction, prefix)
    if a:direction == "up"
        try
            execute a:prefix . "previous"
        catch /^Vim\%((\a\+)\)\=:E553/
            execute a:prefix . "last"
        catch /^Vim\%((\a\+)\)\=:E\%(325\|776\|42\):/
        endtry
    else
        try
            execute a:prefix . "next"
        catch /^Vim\%((\a\+)\)\=:E553/
            execute a:prefix . "first"
        catch /^Vim\%((\a\+)\)\=:E\%(325\|776\|42\):/
        endtry
    endif

    if &foldopen =~ 'quickfix' && foldclosed(line('.')) != -1
        normal! zv
    endif
endfunction
