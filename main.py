# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   				      #
#			          Python Code Editor					   		#
#			          Developer: Carbon				       		#
#													   				      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from tkinter import Tk, PhotoImage, Text, Scrollbar, VERTICAL, RIGHT, Y, Menu, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from idlelib.colorizer import ColorDelegator, make_pat
from idlelib.percolator import Percolator
from os import system, path
from re import compile, S

# Editor Window: #

window = Tk()
window.title("Python Editor: Untitled")
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.geometry(f'{screenWidth // 2}x{screenHeight // 2}')
window.call('tcl_wordBreakAfter', '', 0) 
window.call('set', 'tcl_wordchars', '[a-zA-Z0-9_]')
window.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_]')

# Editor Icon: #

icon = PhotoImage(file = 'logo.png')
window.iconphoto(False, icon)

# Text Editor: #

textEditor = Text(window, font=("Monaco", 15), bg = "#2D3132", fg = "#FFFFFF", undo = True)
textEditor.pack(side = "top", fill = "both", expand = True, padx = 0, pady = 0)

# Text Highlighting: 

highlight = ColorDelegator()
highlight.prog = compile(r'\b(P<MYGROUP>tkinter)\b|' + make_pat(), S)
highlight.idprog = compile(r'\s+(\w+)', S)

highlight.tagdefs['COMMENT'] = {'foreground': '#BACBE7', 'background': '#2D3132'}
highlight.tagdefs['KEYWORD'] = {'foreground': '#5FD66B', 'background': '#2D3132'}
highlight.tagdefs['BUILTIN'] = {'foreground': '#F29020', 'background': '#2D3132'}
highlight.tagdefs['STRING'] = {'foreground': '#1E69EB', 'background': '#2D3132'}
Percolator(textEditor).insertfilter(highlight)

# Scroll Bar: 

scrollBarY = Scrollbar(textEditor, orient = VERTICAL)
scrollBarY.pack(side = RIGHT, fill = Y, padx = 0)
scrollBarY.config(command = textEditor.yview)
textEditor.config(yscrollcommand = scrollBarY.set)

# Editor Variables: #

globalPath = ''

# Editor Functions: #

def runCode():
	global globalPath
	if(globalPath == ''):
		saveAsFile()
	else:
		saveFile()
		command = f'start cmd.exe /k python {globalPath}'
		system(command)

def newFile():
	global globalPath
	textEditor.delete('1.0', END)
	globalPath = ''
	window.title("Python Editor: Untitled")

def openFile():
	global globalPath
	filePath = askopenfilename(filetypes = [('Python Files', '*.py')])
	if(filePath == ''):
			if(globalPath == ''):
				window.title("Python Editor: Untitled")
			else:
				window.title(f"Python Editor: {path.basename(globalPath)}")
			return
	with open(filePath, 'r') as file:
		text = file.read()
		textEditor.delete('1.0', END)
		textEditor.insert('1.0', text)
		file.close()
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def saveFile():
	global globalPath
	if(globalPath == ''):
		filePath = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	else:
		filePath = globalPath
		with open(filePath, 'w') as file:
			text = textEditor.get('1.0', END)
			file.write(text)
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def saveAsFile():
	global globalPath
	filePath = asksaveasfilename(filetypes = [('Python Files', '*.py')])
	if(filePath == ''):
		return
	with open(filePath, 'w') as file:
		text = textEditor.get('1.0', END)
		file.write(text)
	globalPath = filePath
	window.title(f"Python Editor: {path.basename(filePath)}")

def copyText():
   textEditor.event_generate("<<Copy>>")

def cutText():
   textEditor.event_generate("<<Cut>>")

def pasteText():
   textEditor.event_generate("<<Paste>>")

def selectAll():
  	textEditor.tag_add('sel', '1.0', END)

# Menu & Buttons: #

# Run:
menu = Menu(window)

filesBar = Menu(menu, tearoff = 0)
editBar = Menu(menu, tearoff = 0)

# New File:
filesBar.add_command(label = "New File", command = newFile)

# Open:
filesBar.add_command(label = 'Open File', command = openFile)

# Save:
filesBar.add_command(label = 'Save', command = saveFile)

# Save As:
filesBar.add_command(label = 'Save As...', command = saveAsFile)

# Copy: 
editBar.add_command(label = 'Copy (CTRL + C)', command = copyText)

# Cut: 
editBar.add_command(label = 'Cut (CTRL + X)', command = cutText)

# Paste: 
editBar.add_command(label = 'Paste (CTRL + V)', command = pasteText)

# Select All: 
editBar.add_command(label = 'Select All (CTRL + A)', command = selectAll)

# Run:
menu.add_command(label = "Run", command = runCode)

# Add buttons to the their sections:
menu.add_cascade(label = 'Files', menu = filesBar)
menu.add_cascade(label = 'Edit', menu = editBar)

# Config: #

window.config(menu = menu)

# Window Loop: #

window.mainloop()

