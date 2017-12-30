""
" @section Settings

""
" @setting(tcd#snippets_path)
" Full path to the folder containing Ultisnips snippets.
let g:tcd#snippets_path = $HOME . '/.dotfiles/editors/nvim/snipz'


""
" @section Commands

""
" @command(MoveReg)
" @usage `:MoveReg {from} {to}`
" Copies the text {from} one register {to} another.
command! -nargs=+ MoveReg :<C-u> call tcd#ReReg(<f-args>)

""
" @command(CleanCmd)
" Redraws before showing command line completion options.
" command! -nargs=0 CleanCmd call tcd#Redraw()


cnoremap <F6> <C-r>=tcd#Redraw()<CR>
"
" augroup TcdAuto
"   autocmd!
"   autocmd! User UltiSnipsEnterFirstSnippet
"   autocmd User UltiSnipsEnterFirstSnippet echom "SnipEnter"
"   autocmd! User UltiSnipsExitLastSnippet
"   autocmd User UltiSnipsExitLastSnippet echom "SnipExit"
" augroup END

