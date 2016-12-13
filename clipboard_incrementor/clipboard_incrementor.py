from __future__ import print_function
import pythoncom

# to watch keys
import pyHook
# to send keys
import win32com.client
# to get clipboard
import pyperclip

shell = win32com.client.Dispatch("WScript.Shell")

"""
Lcontrol = 162
Rcontrol = 163
Lshift = 160
Rshift = 161
F8 = 119
c = 67
v = 86
"""

def printData(event):
	print('---\n\n')
	print('MessageName:',event.MessageName)
	print('Message:',event.Message)
	print('Time:',event.Time)
	print('Window:',event.Window)
	print('WindowName:',event.WindowName)
	print('Ascii:', event.Ascii, chr(event.Ascii))
	print('Key:', event.Key)
	print('KeyID:', event.KeyID)
	print('ScanCode:', event.ScanCode)
	print('Extended:', event.Extended)
	print('Injected:', event.Injected)
	print('Alt', event.Alt)
	print('Transition', event.Transition)
	print('---\n\n')
	
def incrementNumbers(str):
	str = str.replace('8','9')
	str = str.replace('7','8')
	str = str.replace('6','7')
	str = str.replace('5','6')
	str = str.replace('4','5')
	str = str.replace('3','4')
	str = str.replace('2','3')
	str = str.replace('1','2')
	str = str.replace('0','1')
	return str
	
def OnMouseEvent(event):
	return True
	
def OnKeyboardEvent(event):
	# printData(event)
	
	# if the key is F8
	if event.KeyID == 119:
		print('F8 pressed')
		
		# change clipboard data
		str = pyperclip.paste()
		str = incrementNumbers(str)
		pyperclip.copy(str)
		
		shell.SendKeys("^(v)",1)
	# return True to pass the event to other handlers
	# return False to stop the event from propagating
	return True

	# 0123456789abc
if __name__ == '__main__':
	# create the hook mananger
	hm = pyHook.HookManager()
	# register two callbacks
	hm.MouseAllButtonsDown = OnMouseEvent
	hm.KeyDown = OnKeyboardEvent

	# hook into the mouse and keyboard events
	hm.HookMouse()
	hm.HookKeyboard()
	
	pythoncom.PumpMessages()