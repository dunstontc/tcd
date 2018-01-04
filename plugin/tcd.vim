""
" @section Settings

""
" @setting(g:tcd#snippets_path)
" Full path to the folder containing Ultisnips snippets.
let g:tcd#snippets_path = $HOME . '/nvim.d/snipz'


" if !exists('g:tcd#data_dir')
" ""
" " @setting(g:tcd#data_dir)
" " The location to store files containing saved projects & bookmarks.
"   let g:tcd#data_dir = expand($XDG_CACHE_HOME !=? '' ?
"           \  $XDG_CACHE_HOME . '/tcd' : '~/.cache/tcd')
" endif

let g:tcd#data_dir = '/Users/clay/Projects/Vim/me/tcd/data'

""
" @section Commands

""
" @command(MoveReg)
" `:MoveReg {from} {to}`
" Copies the text {from} one register {to} another.
command! -nargs=+ MoveReg :<C-u> call tcd#ReReg(<f-args>)


