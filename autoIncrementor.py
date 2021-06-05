# OrdiNeu's auto incrementor for Dugnutt
import keyboard
import wx

# Globals
Filename = "test.txt"
Format = "Number of times pressed: {}"
count = 0
hotkey = "ctrl+alt+z"
dehotkey = "ctrl+alt+x"
error = ""
refresh = None

# Callback to automatically write in the text file
def changeCount(amount, auto):
    global count
    global error
    if (auto):
        count += amount
    try:
        with open(Filename, 'w') as f:
            f.write(Format.format(count))
        error = ""

        if refresh is not None:
            refresh()
    except Exception as e:
        error = str(e)

def increment(autoIncrement=True):
    changeCount(+1, autoIncrement)

def decrement(autoDecrement=True):
    changeCount(-1, autoDecrement)

# Setup the Keyboard
keyboard.add_hotkey(hotkey, increment)
keyboard.add_hotkey(dehotkey, decrement)
increment(autoIncrement=False)

# Class for the UI
class IncrementorUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(IncrementorUI, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Filename input
        filenamePanel = wx.Panel(self.panel)
        f_hbox = wx.BoxSizer(wx.HORIZONTAL)
        inputLabel = wx.StaticText(filenamePanel, label="Filename: ")
        self.input = wx.StaticText(filenamePanel, label=Filename)
        self.fileNameSelector = wx.Button(filenamePanel, label="Select")
        self.fileNameSelector.Bind(wx.EVT_BUTTON, self.OpenFileDialog)
        f_hbox.Add(inputLabel, wx.LEFT)
        f_hbox.Add(self.input, wx.EXPAND)
        f_hbox.Add(self.fileNameSelector, wx.RIGHT)
        filenamePanel.SetSizer(f_hbox)

        # Format input
        formatPanel = wx.Panel(self.panel)
        fo_hbox = wx.BoxSizer(wx.HORIZONTAL)
        formatLabel = wx.StaticText(formatPanel, label="Format: ")
        self.format = wx.TextCtrl(formatPanel, value=Format)
        self.format.Bind(wx.EVT_TEXT, self.SetFormat)
        fo_hbox.Add(formatLabel, wx.LEFT)
        fo_hbox.Add(self.format, wx.EXPAND)
        formatPanel.SetSizer(fo_hbox)

        # Count input
        countPanel = wx.Panel(self.panel)
        co_hbox = wx.BoxSizer(wx.HORIZONTAL)
        countLabel = wx.StaticText(countPanel, label="Count: ")
        self.count = wx.SpinCtrl(countPanel, value=str(count), min=-99999999, max=99999999)
        self.count.Bind(wx.EVT_TEXT, self.SetCount)
        co_hbox.Add(countLabel, wx.LEFT)
        co_hbox.Add(self.count, wx.EXPAND)
        countPanel.SetSizer(co_hbox)

        # Hotkey input
        hotkeyPanel = wx.Panel(self.panel)
        hk_hbox = wx.BoxSizer(wx.HORIZONTAL)
        hotkeyLabel = wx.StaticText(hotkeyPanel, label="+1 Hotkey: ")
        self.hotkey = wx.TextCtrl(hotkeyPanel, value=hotkey)
        self.hotkeySelector = wx.Button(hotkeyPanel, label="Set hotkey")
        self.hotkeySelector.Bind(wx.EVT_BUTTON, self.StartListen)
        hk_hbox.Add(hotkeyLabel, wx.LEFT)
        hk_hbox.Add(self.hotkey, wx.EXPAND)
        hk_hbox.Add(self.hotkeySelector, wx.RIGHT)
        hotkeyPanel.SetSizer(hk_hbox)

        # Hotkey input
        dehotkeyPanel = wx.Panel(self.panel)
        dehk_hbox = wx.BoxSizer(wx.HORIZONTAL)
        dehotkeyLabel = wx.StaticText(dehotkeyPanel, label="-1 Hotkey: ")
        self.dehotkey = wx.TextCtrl(dehotkeyPanel, value=dehotkey)
        self.dehotkeySelector = wx.Button(dehotkeyPanel, label="Set hotkey")
        self.dehotkeySelector.Bind(wx.EVT_BUTTON, self.StartDecrementListen)
        dehk_hbox.Add(dehotkeyLabel, wx.LEFT)
        dehk_hbox.Add(self.dehotkey, wx.EXPAND)
        dehk_hbox.Add(self.dehotkeySelector, wx.RIGHT)
        dehotkeyPanel.SetSizer(dehk_hbox)

        # Error input
        self.ErrorLabel = wx.StaticText(self.panel, label=error)

        # Outer panel
        vbox.Add(filenamePanel)
        vbox.Add(formatPanel)
        vbox.Add(countPanel)
        vbox.Add(hotkeyPanel)
        vbox.Add(dehotkeyPanel)
        vbox.Add(self.ErrorLabel)
        self.panel.SetSizer(vbox)

    def OpenFileDialog(self, e):
        global Filename
        with wx.FileDialog(self, 'Select File', wildcard="Text file(*.txt)|*.txt", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            Filename = fileDialog.GetPath()
        self.RefreshUI()

    def RefreshUI(self):
        self.count.Unbind(wx.EVT_TEXT)
        self.format.Unbind(wx.EVT_TEXT)
        self.input.SetLabel(Filename)
        self.count.SetValue(count)
        self.ErrorLabel.SetLabel(error)
        self.count.Bind(wx.EVT_TEXT, self.SetCount)
        self.format.Bind(wx.EVT_TEXT, self.SetFormat)

    def SetFormat(self, e):
        global Format
        Format = e.GetString()
        self.RefreshUI()
        increment(False)

    def SetCount(self, e):
        global count
        count = int(e.GetString())
        self.RefreshUI()
        increment(False)

    def StartListen(self, e):
        self.hotkey.SetValue("Listening for keypress...")
        self.keyboardHook = keyboard.hook(self.EndListen)

    def EndListen(self, e):
        global hotkey
        keyboard.remove_hotkey(hotkey)

        # Only remove the listen status if it isn't a modifier
        hotkey = keyboard.get_hotkey_name()
        keyboard.add_hotkey(hotkey, increment)

        if not keyboard.is_modifier(e.name):
            keyboard.unhook(self.keyboardHook)
        self.hotkey.SetValue(hotkey)
        self.RefreshUI()
        increment(False)

    def StartDecrementListen(self, e):
        self.dehotkey.SetValue("Listening for keypress...")
        self.deKeyboardHook = keyboard.hook(self.EndDecrementListen)

    def EndDecrementListen(self, e):
        global dehotkey
        keyboard.remove_hotkey(dehotkey)

        # Only remove the listen status if it isn't a modifier
        dehotkey = keyboard.get_hotkey_name()
        keyboard.add_hotkey(dehotkey, decrement)

        if not keyboard.is_modifier(e.name):
            keyboard.unhook(self.deKeyboardHook)
        self.dehotkey.SetValue(dehotkey)
        self.RefreshUI()
        decrement(False)

app = wx.App()
frame = IncrementorUI(None, title="OrdiNeu's Auto-incrementor for Dugnutt", style=wx.CLOSE_BOX | wx.CAPTION | wx.RESIZE_BORDER)
refresh = frame.RefreshUI
frame.Show()

app.MainLoop()
