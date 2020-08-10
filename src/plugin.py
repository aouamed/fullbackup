from Components.ActionMap import ActionMap
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.Screen import Screen
from Tools.Directories import fileExists
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigSelection, NoSave
import os

class Full_main(Screen, ConfigListScreen):
    skin = """
             <screen position="center,center" size="902,340" title="Full Backup">
             <widget name="config" position="30,10" size="840,60" scrollbarMode="showOnDemand"/>
             <widget name="lab1" position="30,70" size="840,60" font="Regular;24" valign="center" transparent="1"/>
             <ePixmap pixmap="skin_default/buttons/red.png" position="200,290" size="140,40" alphatest="on"/>
             <ePixmap pixmap="skin_default/buttons/green.png" position="550,290" size="140,40" alphatest="on"/>
             <widget name="key_red" position="200,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
             <widget name="key_green" position="550,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
             </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Backup'))
        self['lab1'] = Label('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.doBackUp,
         'red': self.close,
         'back': self.close})
        self.updateList()
        self.deviceok = True

    def updateList(self):
        myusb = myusb2 = myhdd = ''
        myoptions = []
        if fileExists('/proc/mounts'):
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                elif line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                elif line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'

            f.close()
        if myusb:
            myoptions.append((myusb, myusb))
        if myusb2:
            myoptions.append((myusb2, myusb2))
        if myhdd:
            myoptions.append((myhdd, myhdd))
        self.list = []
        self.my_path = NoSave(ConfigSelection(choices=myoptions))
        my_path = getConfigListEntry(_('Path to store Full Backup'), self.my_path)
        if len(myoptions) > 0:
            self.list.append(my_path)
            self['config'].list = self.list
            self['config'].l.setList(self.list)
        else:
            self['lab1'].setText(_('Sorry no device found to store backup.'))
            self.deviceok = False

    def doBackUp(self):
        if self.my_path.value:
            mytitle = _('Full Backup on: ') + self.my_path.value
            if not fileExists('/usr/bin/fullbackup.sh'):
                os.system('cp -r /usr/lib/enigma2/python/Plugins/Extensions/FullBackup/fullbackup.sh /usr/bin')
                os.system('chmod -R 0755 /usr/bin/fullbackup.sh')
            cmd = '/usr/bin/fullbackup.sh ' + self.my_path.value
            self.session.open(Console, title=mytitle, cmdlist=[cmd], finishedCallback=self.myEnd)
        else:
            self.session.open(MessageBox, _('Sorry no device found to store backup.'), MessageBox.TYPE_INFO)

    def myEnd(self):
        self.close()


def main(session, **kwargs):
    session.open(Full_main)


def menu(menuid, **kwargs):
    if menuid == 'system':
        return [(_('Full Backup'),
          main,
          'FullBackup',
          1)]
    return []


def Plugins(**kwargs):
    return PluginDescriptor(name='FullBackup', description=_('Full image backup'), where=PluginDescriptor.WHERE_MENU, fnc=menu)
