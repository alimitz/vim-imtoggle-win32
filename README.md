# vim-imtoggle-windows
vim plugin for change input methods under win32 os

By this python script, it can automatically change your input methods between toggling with insert mode and normal mode.

1. The first, you need install python3 and win32api for python.
2. download im.py
3. You need type the follow into you .vimrc:
   if ($OS_TYPE == "windows")
	    autocmd InsertEnter * :!start /b im.py restore
	    autocmd InsertLeave * :!start /b im.py en
   endif
4. Add two env into you win32 system: 
   $VIM_HOME : point to your .vim/ directory.
   $PATH: point to the directory storing the im.py
5. Probe your input language: '
   In the command console, type "im.py pim", to list the language list of you windows os. 
   Then modify "Class Lan(emun)" items of    im.py relating to your own os.
6. If nessary, you need type "im.py pwin", to list out all window title, 
   then select the vim one, modify win32gui.FindWindow('Vim',None).
