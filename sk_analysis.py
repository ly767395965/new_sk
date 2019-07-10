#!/usr/bin/python3
import wx
import os
import time
import moudle_path
import timeControl
import excelOp
import skOp

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 600))
        filemenu = wx.Menu()
        menuStart = filemenu.Append(wx.ID_ABOUT, '&开始')
        filemenu.AppendSeparator()  # 菜单条的线
        menuExit = filemenu.Append(wx.ID_EXIT, '&退出')
        menuStop = filemenu.Append(wx.ID_EXIT, '&停止')

        skmenu = wx.Menu()
        menuAllsk = skmenu.Append(wx.ID_ANY, '&all', '查看所有sk的情况')
        menusk1 = skmenu.Append(wx.ID_ANY, '&sk1', '查看sk1的情况')
        menusk2 = skmenu.Append(wx.ID_ANY, '&sk2', '查看sk2的情况')

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, '&File')  # 在菜单中加入file操作, 并把filemenu 菜单栏加入该操作中
        menuBar.Append(skmenu, '&SK')  # 在菜单中加入file操作, 并把filemenu 菜单栏加入该操作中
        self.SetMenuBar(menuBar)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)  # 设置查看具体sk sizer
        buttons = wx.Button(self, -1, "check ans")
        self.input = wx.TextCtrl(self)
        self.sizer2.Add(self.input, 1, wx.EXPAND)
        self.sizer2.Add(buttons, 1, wx.EXPAND)

        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)  # 设置sk分析信息 sizer
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(399, 400))  # 设置文本编辑域
        # self.import_view = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(1, 400))
        self.sizer3.Add(self.control, 1, wx.FIXED_MINSIZE)
        # self.sizer3.Add(self.import_view, 0.1, wx.FIXED_MINSIZE)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.sizer3, 0, wx.FIXED_MINSIZE)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Bind(wx.EVT_MENU, self.onStart, menuStart)  # 绑定事件 wx.EVT_MENU 表示绑定是菜单事件
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_BUTTON, self.querySkAnalysis, buttons)

        self.timer = wx.Timer(self)  # 创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  # 绑定一个定时器事件
        self.Show(True)

    def onStart(self, even):
        self.timer.Start(1000)
        self.control.SetInsertionPoint(0)
        self.control.WriteText('系统启动\r\n')

    def onExit(self, even):
        self.Close()

    def openFile(self, even):
        self.dirname = ''
        dlg = wx.FileDialog(self, 'Choose a file', self.dirname, '', '*.*', wx.ID_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()

        dlg.Destroy()

    def querySkAnalysis(self, e):
        print('喝了咯')

    def OnTimer(self, even):
        skop_obj = skOp.skOpC()
        data = skop_obj.dateAnalysis()
        self.control.Clear()
        data_len = len(data)
        if data_len > 20:
            data_len = 20
        i = 0
        while i < data_len:
            val = data[i]
            start_time = str(val['start_time'])
            stop_time = str(val['now_time'])
            s_d = skop_obj.timeDiff(start_time, stop_time)
            per = round(val['per'], 3)
            s_d = str(s_d)
            per = str(per)
            text = '' + start_time + ' - ' + stop_time + ' sec:' + s_d + '  pp:' + per
            self.control.WriteText(text + '\r\n')
            i += 1
        self.timer.Start(15000)


app = wx.App()
frame = MyFrame(None, 'editor')
app.MainLoop()
