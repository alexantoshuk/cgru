# -*- coding: utf-8 -*-

import sys
import os

if sys.platform.find('win') == 0 and sys.executable.find('pythonw') != -1:
	try:
		sys.stdout = open('c:\\temp\\cgru_keeper_log.txt', 'w')
		sys.stderr = sys.stdout
	except:
		pass

# Write qt.conf file on MS Windows:
# Python/PySide needs Prefix = site-packages/PySide*, while afwatch needs CGRU/dll
# (dll/ ships only Core/Gui/Widgets/Network/Multimedia used by afwatch).
if sys.platform.find('win') == 0:
	cgru_loc = os.getenv('CGRU_LOCATION')
	af_root = os.getenv('AF_ROOT')

	def _write_qt_conf(path, prefix):
		qtconf_dir = os.path.dirname(path)
		if qtconf_dir and not os.path.isdir(qtconf_dir):
			try:
				os.makedirs(qtconf_dir)
			except Exception:
				return
		try:
			if os.path.isfile(path):
				os.remove(path)
			with open(path, mode='w') as qtconf_file:
				qtconf_file.write('[Paths]\nPrefix = %s\n' % prefix)
		except Exception as err:
			print('WARNING: Can`t write "%s": %s' % (path, err))

	pyside = os.path.join(sys.prefix, 'Lib', 'site-packages', 'PySide6')
	if not os.path.isdir(pyside):
		pyside = os.path.join(sys.prefix, 'Lib', 'site-packages', 'PySide2')
	dll_prefix = None
	if cgru_loc and os.path.isdir(os.path.join(cgru_loc, 'dll')):
		dll_prefix = cgru_loc.replace('\\', '/') + '/dll'
	python_prefix = pyside.replace('\\', '/') if os.path.isdir(pyside) else dll_prefix
	if python_prefix is None:
		python_prefix = (cgru_loc.replace('\\', '/') + '/dll') if cgru_loc else 'dll'
	if dll_prefix is None:
		dll_prefix = python_prefix
		if os.path.isdir(pyside):
			print('WARNING: CGRU dll/ not found, using Qt from: ' + dll_prefix)

	_write_qt_conf(sys.prefix + '/qt.conf', python_prefix)
	if af_root:
		_write_qt_conf(os.path.join(af_root, 'bin', 'qt.conf'), dll_prefix)
if sys.platform.find('darwin') == 0:
    try:
        import AppKit
        info = AppKit.NSBundle.mainBundle().infoDictionary()
        info["LSBackgroundOnly"] = "1"
    except:
        print("WARNING: pyobjc-framework-Cocoa is not installed, can't hide dock icon.")

import Qt
from Qt import QtWidgets

print('Qt: ' + ('%s %s (%s)' % ( Qt.__qt_version__, Qt.__binding__, Qt.__binding_version__)))

import cgruconfig
import cmd
from refresh import Refresh
import render
from tray import Tray
from server import Server
import serverhttps


# Define keeper launch command if was not:
keeper_cmd = os.getenv('CGRU_KEEPER_CMD')
if keeper_cmd is None:
	keeper_cmd = '"%s" "%s"' % (os.getenv('CGRU_PYTHONEXE'), sys.argv[0])
cgruconfig.VARS['CGRU_KEEPER_CMD'] = keeper_cmd

# Create tray application with refresh:
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
cmd.Application = app
serverhttps.serve(cgruconfig.VARS['keeper_port_https'])
cmd.Tray = Tray(app)
refresh = Refresh(app)
render.Refresh = refresh
server = Server()
# PySide6: exec(); PySide2: exec_()
getattr(app, 'exec', getattr(app, 'exec_', None))()
