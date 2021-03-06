highlight RBP1 guibg=Red ctermbg=red
highlight RBP2 guibg=Yellow ctermbg=yellow
highlight RBP3 guibg=Green ctermbg=green
highlight RBP4 guibg=Blue ctermbg=blue
let g:rainbow_levels = 4
function! RainbowParens(cmdline)
  let ret = []
  let i = 0
  let lvl = 0
  while i < len(a:cmdline)
    if a:cmdline[i] is# '('
      call add(ret, [i, i + 1, 'RBP' . ((lvl % g:rainbow_levels) + 1)])
      let lvl += 1
    elseif a:cmdline[i] is# ')'
      let lvl -= 1
      call add(ret, [i, i + 1, 'RBP' . ((lvl % g:rainbow_levels) + 1)])
    endif
    let i += 1
  endwhile
  return ret
endfunction
call input({'prompt':'>','highlight':'RainbowParens'})
