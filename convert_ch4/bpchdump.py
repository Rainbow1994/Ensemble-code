#! /geos/u23/epd/bin/python2.5

try:
    import wx
except ImportError:
    print '*'*30+'WARNING'+'*'*30
    print 'Incorrect Python version!' 
    print 'please use ./bpchdump.py'
    print '*'*80
    exit()



from numpy import *
from pylab import *

import geos_chem_def as gcdf
import time_module as tm
import bpch2_rw_v2_wx as bpch2_mod
import os
import images
import wx.py as pysh

file_idd=list()
file_idd.append(0)
print file_idd

cur_l={}
cur_d=None

test_d=300.0


ID_LOAD=120
ID_EXIT=110
ID_SAVEDEF=140
ID_SAVE_SETTING=150
ID_ABOUT=101
ID_SET=130
ID_BROWSE=210
ID_BROWSE_TRACER=220
ID_BROWSE_DIAG=230



default_setting_file=os.path.expanduser('~')+'/.bpchwx'

class MyFileDialog_info(wx.Dialog):
    def __init__(self, parent, ID, title, defDir,
                 defTracer="", \
                 defDiag="", \
                 size=wx.DefaultSize, pos=wx.DefaultPosition, \
                 style=wx.DEFAULT_DIALOG_STYLE, useMetal=False):
        
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.

        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)
            
        
        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.dirname=defDir
        
        # box = wx.BoxSizer(wx.HORIZONTAL)

        gs = wx.GridSizer(2, 3)
        
        flnmlabel = wx.StaticText(self, -1, "TacerInfo:")
        flnmlabel.SetHelpText("File Name")
        gs.Add(flnmlabel, 0, wx.ALIGN_CENTRE|wx.ALL, 0)

        self.tracertext = wx.TextCtrl(self, -1, "", size=(250,30))
        self.tracertext.SetHelpText("Enter Tracer Info File Name")
        self.tracertext.SetValue(defTracer)
        gs.Add(self.tracertext, 1,  wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND,0)
        
        
        
        browsebtn_tracer=wx.Button(self, ID_BROWSE_TRACER, "Browse",  size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Browse_tracer, browsebtn_tracer)
        gs.Add(browsebtn_tracer, 0,  wx.ALIGN_CENTRE|wx.ALL,0)
        
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        

        # box = wx.BoxSizer(wx.HORIZONTAL)

        flnmlabel = wx.StaticText(self, -1, "DiagInfo:")
        flnmlabel.SetHelpText("File Name")
        gs.Add(flnmlabel, 0,  wx.ALIGN_CENTRE|wx.ALL,  0)

        self.diagtext = wx.TextCtrl(self, -1, "", size=(250,30))
        self.diagtext.SetHelpText("Enter Tracer Info File Name")
        self.diagtext.SetValue(defDiag)
        gs.Add(self.diagtext, 1, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 0)
        
        
        browsebtn_diag=wx.Button(self, ID_BROWSE_DIAG, "Browse",  size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Browse_diag, browsebtn_diag)
        gs.Add(browsebtn_diag, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add(gs, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        
        # if wx.Platform != "__WXMSW__":
        #    btn = wx.ContextHelpButton(self)
        #     btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
    
    def OnClick_Browse_tracer(self, event):
        wildcard = "data files (tra*.dat) |tra*.dat | All files (*.*)|*.*"
        dirname=self.dirname.strip()
        if (dirname==""):
            dirname=os.getcwd()
        
        
        dlg=wx.FileDialog(self, "Choose Tracer Info", dirname, "", wildcard=wildcard, \
                          style=wx.FD_OPEN | wx.CHANGE_DIR)
        dlg.SetFilterIndex(1)
        
        if (dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            full_name=os.path.join(dirname, filename)
            self.tracertext.SetValue(full_name)
            
        dlg.Destroy()
        return False

    def OnClick_Browse_diag(self, event):
        wildcard = "data files (diag*.dat) |diag*.dat | All files (*.*) |*.*"
        
        dirname=self.dirname.strip()
        if (dirname==""):
            dirname=os.getcwd()
        
        dlg=wx.FileDialog(self, "Choose Diag Info", dirname, "", wildcard=wildcard, \
                          style=wx.FD_OPEN | wx.CHANGE_DIR)
        dlg.SetFilterIndex(1)
        
        if (dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            full_name=os.path.join(dirname, filename)
            self.diagtext.SetValue(full_name)
            
        dlg.Destroy()
        return False

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):

        # the setting need to keep
        self.dirname=""
        self.flnm=""
        self.tracerinfo="/geos/u23/enkf_std/diaginfo.dat"
        self.diaginfo="/geos/u23/enkf_std/tracerinfo.dat"
        self.bpdata_list=None
        self.ifig=0
        
        try:
            deffile=open(default_setting_file, 'r')
            lines=deffile.readlines()
            deffile.close()
            
            for line in lines:
                if 'DIR:' in line:
                    terms=line.split()
                    self.dirname=terms[1].strip()
                elif 'FLNM' in line:
                    terms=line.split()
                    self.flnm=terms[1].strip()
                elif ('TRACERINFO:' in line):
                    terms=line.split()
                    self.tracerinfo=terms[1].strip()
                elif ('DIAGINFO:' in line):
                    terms=line.split()
                    self.diaginfo=terms[1].strip()
                    
                    
        except IOError:
            self.dirname="/geos/u23/enkf_std/enkf_output/"
            self.flnm="restart.EN0001-EN0024.20030101"
            self.fullname=self.dirname+self.flnm
            self.tracerinfo="/geos/u23/enkf_std/enkf_output/diaginfo.EN0001-EN0024.dat"
            self.diaginfo="/geos/u23/enkf_std/enkf_output/tracerinfo.EN0001-EN0024.dat"
        
        if (self.dirname in self.flnm):
            self.fullname=self.flnm
        else:
            self.fullname=self.dirname+'/'+self.flnm
        
        
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(880,800))
        # self.control=wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        
        self.CreateStatusBar()
        
        filemenu=wx.Menu()
        filemenu.Append(ID_LOAD, "&Load", "Load BPCH2 FILE")
        filemenu.Append(ID_SAVE_SETTING, "&Save Setting", "Save Current Settings")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT, "E&xit", "Terminate the program")
        
        setmenu=wx.Menu()
        setmenu.Append(ID_SET, "Ch&oose Info", "Set Tracer & Diag Info files")
        helpmenu=wx.Menu()
        helpmenu.Append(ID_ABOUT, "&About", "About wx BPCH dump")
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(setmenu, "&Configure")
        menuBar.Append(helpmenu, "&Help")
        
        
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_LOAD, self.OnLoad)
        wx.EVT_MENU(self, ID_SAVE_SETTING, self.OnSaveSetting)
        wx.EVT_MENU(self, ID_SET, self.OnSet)
        self.SetMenuBar(menuBar)
        # set up the list box
        

        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.getSmilesBitmap())
        self.sm_up = self.il.Add(images.getSmallUpArrowBitmap())
        self.sm_dn = self.il.Add(images.getSmallDnArrowBitmap())
        bmp_browse=wx.Bitmap('/geos/u23/enkf_std/minus4.ico')
        

        panel_w=wx.Panel(self,-1)
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        panel_file=wx.Panel(panel_w, -1)
        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        
        label_file=wx.StaticText(panel_file, -1, 'File Name:')
        hbox1.Add(label_file, 0, wx.ALL|wx.ALIGN_RIGHT,10)
        self.text_file=wx.TextCtrl(panel_file, -1, size=(-1, 30))
        self.text_file.SetValue(self.fullname)
        hbox1.Add(self.text_file, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE_HORIZONTAL|wx.EXPAND,10)
        self.browsebtn=wx.BitmapButton(panel_file, ID_BROWSE, bmp_browse,  size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Browse, self.browsebtn)
        hbox1.Add(self.browsebtn, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT,10)
        
        self.loadbtn=wx.Button(panel_file, ID_LOAD, "Load",  size=(60, 30))
        hbox1.Add(self.loadbtn, 0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self.OnLoad, self.loadbtn)
        
        
        panel_file.SetSizer(hbox1)
        vbox.Add(panel_file, 0, wx.ALL|wx.EXPAND, 1)
        
        

        
        panel_list=wx.Panel(panel_w, -1)
        
                
        self.infolist=wx.ListCtrl(panel_list, -1, style=wx.LC_REPORT)
        self.currentItem=-1
        
        self.infolist.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        self.infolist.InsertColumn(0, 'No')
        self.infolist.InsertColumn(1, 'Category')
        self.infolist.InsertColumn(2, 'Name')
        self.infolist.InsertColumn(3, 'Unit')
        self.infolist.InsertColumn(4, 'TAU0')
        self.infolist.InsertColumn(5, 'TAU1')
        self.infolist.InsertColumn(6, 'NX')
        self.infolist.InsertColumn(7, 'NY')
        self.infolist.InsertColumn(8, 'NZ')
        self.infolist.InsertColumn(9, 'Max')
        self.infolist.InsertColumn(10, 'Min')
        
         
        
        
        
        self.infolist.SetColumnWidth(0, 80)
        self.infolist.SetColumnWidth(1, 80)
        self.infolist.SetColumnWidth(2, 80)
        self.infolist.SetColumnWidth(3, 80)
        self.infolist.SetColumnWidth(4, 100)
        self.infolist.SetColumnWidth(5, 100)
        self.infolist.SetColumnWidth(6, 40)
        self.infolist.SetColumnWidth(7, 40)
        self.infolist.SetColumnWidth(8, 40)
        self.infolist.SetColumnWidth(9, 120)
        self.infolist.SetColumnWidth(10, 120)

        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.infolist)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.infolist)
        # self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.infolist)

        
        self.infolist.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.infolist, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 1)
        sizer.Add((-1, 5))
        panel_list.SetSizer(sizer)

        vbox.Add(panel_list,1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)

        panel_vals=wx.Panel(panel_w, -1)

        hbox=wx.BoxSizer(wx.HORIZONTAL)
        
        label_x=wx.StaticText(panel_vals, -1, 'IX:', size=(30,30))
        hbox.Add(label_x, 0, wx.ALL|wx.ALIGN_RIGHT,10)
        self.text_x=wx.TextCtrl(panel_vals, -1, style=wx.TE_PROCESS_ENTER, size=(-1, 30))
        hbox.Add(self.text_x, 1, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND,10)
        self.text_x.SetValue('0')
        self.text_x.Enable(False)
        self.text_x.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter_x)
        self.text_x.Bind(wx.EVT_KILL_FOCUS, self.EvtTextKillFocus_x)
        
          
        label_y=wx.StaticText(panel_vals, -1, 'IY:', size=(30,30))
        hbox.Add(label_y, 0, wx.ALL|wx.ALIGN_RIGHT,10)
        self.text_y=wx.TextCtrl(panel_vals, -1, style=wx.TE_PROCESS_ENTER,size=(-1, 30))
        hbox.Add(self.text_y, 1, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND,10)
        self.text_y.SetValue('0')
        self.text_y.Enable(False)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter_y, self.text_y)
        self.text_y.Bind(wx.EVT_KILL_FOCUS, self.EvtTextKillFocus_y)
        
        
        label_z=wx.StaticText(panel_vals, -1, 'IZ:', size=(30,30))
        hbox.Add(label_z, 0, wx.ALL|wx.ALIGN_RIGHT,10)
        self.text_z=wx.TextCtrl(panel_vals, -1,style=wx.TE_PROCESS_ENTER,size=(-1,30))
        hbox.Add(self.text_z, 1, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND,10)
        self.text_z.SetValue('0')
        self.text_z.Enable(False)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter_z, self.text_z)
        self.text_z.Bind(wx.EVT_KILL_FOCUS, self.EvtTextKillFocus_z)
        
        
        label_v=wx.StaticText(panel_vals, -1, 'VAL:', size=(60,30))
        hbox.Add(label_v, 0, wx.ALL|wx.ALIGN_LEFT,10)
        self.text_v=wx.TextCtrl(panel_vals, -1 , size=(-1,30))
        hbox.Add(self.text_v, 1, wx.ALL|wx.ALIGN_LEFT|wx.EXPAND,10)
        self.text_v.Enable(False)
        self.ix, self.iy, self.iz=0,0,0
        
        panel_vals.SetSizer(hbox)
        # panel python  #
            
        vbox.Add(panel_vals, 0, wx.ALL|wx.EXPAND, 1)
        self.err_on=False

        self.panel_cmd=wx.Panel(panel_w, -1)
        # locals={'cur_l':cur_l, 'test_d':test_d}
        # self.myshell=pysh.shell.Shell(self.panel_cmd, -1,locals=locals, size=(850, 300))
        # help(self.myshell)
        self.myshell=pysh.shell.Shell(self.panel_cmd, -1 ,size=(850, 300))
        
        # vbox.Add(self.panel_cmd, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE_HORIZONTAL, 10)
        # vbox.Add(self.panel_cmd, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE_HORIZONTAL, 10)
        
        vbox.Add(self.panel_cmd, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_LEFT, 10)
        
        vbox.Add((-1, 5))
        panel_w.SetSizer(vbox)
        
        # panel list
        
        self.Centre()
        
        self.Show(True)
    def OnAbout(self, event):
        d=wx.MessageDialog(self, "The program to read bpch files", "BPCH Dump", wx.OK)
        d.ShowModal()
        d.Destroy()
    def OnSaveSetting(self, event):
        deffile=open(default_setting_file, 'w')
        deffile.write('DIR: '+self.dirname+'\n')
        deffile.write('FLNM: '+self.flnm+'\n')
        deffile.write('TRACERINFO: '+self.tracerinfo+'\n')
        deffile.write('DIAGINFO: '+self.diaginfo+'\n')
        deffile.close()
    
    def OnExit(self, event):
        # save the current file
        
        self.Close(True)

    def OnItemSelected(self, event):
        ##print event.GetItem().GetTextColour()
        
        self.currentItem = event.m_itemIndex
        cur_data=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(cur_data.data)
        
        self.text_x.Enable(True)
        self.text_y.Enable(True)
        self.text_z.Enable(True)
        ix, iy, iz=0,0,0
        self.ix, self.iy, self.iz=ix,iy,iz
        
        
        self.text_x.SetValue(str(ix))
        self.text_y.SetValue(str(iy))
        self.text_z.SetValue(str(iz))
        
        val=cur_data.data[ix, iy, iz]
        self.text_v.SetValue(str(val))
        cur_d=cur_data
        
        
        event.Skip()

    def OnItemDeselected(self, evt):
        self.currentItem=-1
        self.text_x.Enable(False)
        self.text_y.Enable(False)
        self.text_z.Enable(False)
        cur_d=None
        
        
    def OnDoubleClick(self, event):
        if (self.currentItem>=0):
            bpdata=self.bpdata_list[self.currentItem]
            figure(self.ifig)
            self.ifig=self.ifig+1
            subplot(2,1,1)
            bpdata.display(0, show_map=1)
            
            # print 'I am here'
    
    def EvtTextEnter_x(self, event):
#        print 'Here is me'
        
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        ix=self.text_x.GetValue()
#        print ix
#        print nx
        
        IsValid=False
        try:
            ix=int(ix)
            if (ix<nx):
                IsValid=True
                 
        except ValueError:
            pass
        
        if (not IsValid):

            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid X Value', 'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_x.SetFocus()
            # self.err_on=False
            
            # return True
        
        else:
            self.ix=ix
            val=bpdata.data[self.ix, self.iy, self.iz]
            self.text_v.SetValue(str(val))
        
        event.Skip()

    def EvtTextKillFocus_x(self, event):
        if (self.err_on):
            event.Skip()
            return
        
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        ix=self.text_x.GetValue()
        IsValid=False
        try:
            ix=int(ix)
            if (ix<nx):
                IsValid=True
            
        except ValueError:
            pass
        
        if (not IsValid):
            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid X Value',\
                                   'Error',\
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_x.SetFocus()
            # self.err_on=False
            
         #   return True
        
        else:
            self.ix=ix
            

        # self.text_x.SetValue(str(self.ix))
        
                           
        
        event.Skip()
    
    
    def EvtTextEnter_y(self, event):
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        iy=self.text_y.GetValue()
        IsValid=False
        try:
            iy=int(iy)
            if (iy<ny):
                IsValid=True
                 
        except ValueError:
            pass
        
        if (not IsValid):
            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid Y Value', 'Error',                           
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_y.SetFocus()
            # self.err_on=False
            # return True
        
        else:
            self.iy=iy
            val=bpdata.data[self.ix, self.iy, self.iz]
            self.text_v.SetValue(str(val))
        
        event.Skip()

    def EvtTextKillFocus_y(self, event):
        if (self.err_on):
            event.Skip()
            return
        
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        iy=self.text_y.GetValue()
        IsValid=False
        try:
            iy=int(iy)
            if (iy<ny):
                IsValid=True
            
        except ValueError:
            pass
        
        if (not IsValid):
            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid Y Value',\
                                   'Error',\
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_y.SetFocus()
            # self.err_on=False
            
            # return True
        
        else:
            self.iy=iy
            
        
                           
        
        event.Skip()
    
    def EvtTextEnter_z(self, event):
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        iz=self.text_z.GetValue()
        IsValid=False
        try:
            iz=int(iz)
            if (iz<nz):
                IsValid=True
                 
        except ValueError:
            pass
        
        if (not IsValid):
            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid Z Value','Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_z.SetFocus()
            #    return True
            # self.err_on=False
        else:
            self.iz=iz
            val=bpdata.data[self.ix, self.iy, self.iz]
            print val
            self.text_v.SetValue(str(val))
            
        event.Skip()
        

    def EvtTextKillFocus_z(self, event):

        if (self.err_on):
            event.Skip()
            print 'I am here'
            return True
        
        bpdata=self.bpdata_list[self.currentItem]
        nx, ny, nz=shape(bpdata.data)
        iz=self.text_z.GetValue()
        IsValid=False
        try:
            iz=int(iz)
            if (iz<nz):
                IsValid=True
            
        except ValueError:
            pass
        
        if (not IsValid):
            # self.text_y.SetFocus()
            self.err_on=True
            dlg = wx.MessageDialog(self, 'Invalid Z Value',\
                                   'Error',\
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.text_z.SetFocus()
            # self.err_on=False
            
        
        else:
            self.iz=iz
            
        # self.text_z.SetValue(str(self.iz))
        
                           
        
        event.Skip()
    
    
    def OnLoad(self, event):
        self.fullname=self.text_file.GetValue()
        self.dirname=self.dirname
        self.flnm=self.fullname
        
        self.currentItem=-1
        
        ftracerinfo=self.tracerinfo
        fdiaginfo=self.diaginfo
        flnm=self.fullname.strip()
            
        print flnm
        print ftracerinfo
        print fdiaginfo
        
        bpch2=bpch2_mod.bpch2_file_rw(flnm, 'r', do_read=1, \
                                      ftracerinfo=ftracerinfo, \
                                      fdiaginfo=fdiaginfo)
        all_list=list()
        # bpch2.print_datainfo()
        tracers=None
        categorys=None
        taus=None
        tranames=None
        if (self.bpdata_list<>None):
            self.infolist.DeleteAllItems()
        bpdata_list, found=bpch2.get_data(tracers=tracers, categorys=categorys, taus=taus, tranames=tranames)
        self.bpdata_list=bpdata_list
        j=0
        print file_idd
        nfile=len(file_idd)
        cur_file_id=file_idd[nfile-1]
        cur_file_id=cur_file_id+1
        file_idd.append(cur_file_id)
        
        sfile_idd=r'file_%2.2d' % (cur_file_id)
        # for item in bpdata_list:
        #    cur_l.append(item)
        cur_l.update({sfile_idd:bpdata_list})
        # self.myshell.Execute("local_cur_l=cur_l")
        # self.myshell.Destroy()
        # locals={'cur_l':cur_l, 'test_d':test_d}
        # self.myshell=pysh.shell.Shell(self.panel_cmd, -1,locals=locals, size=(850, 300))
        # self.myshell=pysh.shell.Shell(self.panel_cmd, -1,size=(850, 300))
        
        self.myshell.Execute("print 'loaded data stored in the dict  cur_l with', file_idd")
        self.myshell.Execute("print cur_l.keys()")
        # self.myshell.Execute("print shape(cur_l[0].data)")
        
        
        #  self.myshell.Execute("print 'selected  data in cur_d'")
        # self.myshell.Execute("print test_d")
        
        # help(self.myshell)
        
        for bpdata in bpdata_list:
            traname, tau0, tau1=bpdata.get_attr(['name', 'tau0', 'tau1'])
            
            # utc0=tm.tai85_to_utc(3600.0*tau0)
            # utc1=tm.tai85_to_utc(3600.0*tau1)
            # utc0='<'+utc0+'>'
            # utc1='<'+utc1+'>'
            # print bpdata.ntracer, bpdata.category, traname, bpdata.unit, utc0, utc1, shape(bpdata.data), max(bpdata.data.flat),\
            #      min(bpdata.data.flat)
            dix, diy, diz=shape(bpdata.data)
            gpmaxval=max(bpdata.data.flat)
            gpminval=min(bpdata.data.flat)
            sj=r'%2.2d' % (j+1)
            stau0=r'%10.2f' % (tau0)
            stau1=r'%10.2f' % (tau1)
            six=r'%d' % dix
            siy=r'%d' % diy
            siz=r'%d' % diz
            smax='%7.5e' % (gpmaxval)
            smin='%7.5e' % (gpminval)
            
            self.infolist.InsertStringItem(j, sj)
            self.infolist.SetStringItem(j, 1, traname)
            self.infolist.SetStringItem(j, 2, bpdata.category)
            self.infolist.SetStringItem(j, 3, bpdata.unit)
            self.infolist.SetStringItem(j, 4, stau0)
            self.infolist.SetStringItem(j, 5, stau1)
            self.infolist.SetStringItem(j, 6, six)
            self.infolist.SetStringItem(j, 7, siy)
            self.infolist.SetStringItem(j, 8, siz)
            self.infolist.SetStringItem(j, 9, smax)
            self.infolist.SetStringItem(j, 10, smin)
            
            if (j % 2) == 0:
                self.infolist.SetItemBackgroundColour(j, '#e6f1f5')
                                
            if diz ==1:
                self.infolist.SetItemImage(j, self.idx1)
            else:
                self.infolist.SetItemImage(j, self.sm_dn)
            j=j+1
    
              
        
                
    def OnClick_Browse(self, event):
        wildcard = "bpch file (*.bpch)|*.bpch |data files (*.dat) |*.dat | All files (*.*)|*.*"
        
        dirname=self.dirname.strip()
        if (dirname==""):
            dirname=os.getcwd()
            
        dlg=wx.FileDialog(self, "Choose a bpch file", dirname, "", wildcard=wildcard, \
                          style=wx.FD_OPEN | wx.CHANGE_DIR)
        
        dlg.SetFilterIndex(2)
        
        if (dlg.ShowModal()==wx.ID_OK):
            filename=dlg.GetFilename()
            dirname=dlg.GetDirectory()
            full_name=os.path.join(dirname, filename)
            self.dirname=dirname
            self.text_file.SetValue(full_name)
        
        dlg.Destroy()
        

                

    def OnSet(self, event):
        dlg = MyFileDialog_info(self, -1, "Setting", defDir=self.dirname,\
                                defTracer=self.tracerinfo,\
                                defDiag=self.tracerinfo,\
                                size=(450, 300),\
                                style=wx.DEFAULT_DIALOG_STYLE \
                                )
        
        dlg.CenterOnScreen()
        
        val = dlg.ShowModal()
        
        if val == wx.ID_OK:
            self.tracerinfo=dlg.tracertext.GetValue()
            self.diaginfo=dlg.diagtext.GetValue()
            print self.tracerinfo
            print self.diaginfo
            
            
        dlg.Destroy()
    
          
app=wx.PySimpleApp()
frame=MainWindow(None, -1, "BPCH Reader")
app.MainLoop()

        
