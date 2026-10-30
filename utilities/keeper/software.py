# -*- coding: utf-8 -*-
import os
import sys
import time

import cgruconfig
import cgruutils

from Qt import QtCore, QtGui, QtWidgets, QtCompat

Names = ['Blender','Clarisse','Houdini','Maya','Natron','Nuke','NukeX']

if 'windows' in cgruconfig.VARS['platform']:
    Names.extend(['3DSMax','Fusion','Softimage', "Lightwave"])
if 'windows' in cgruconfig.VARS['platform'] \
    or 'macosx' in cgruconfig.VARS['platform']:
    Names.extend(['C4D','AfterFX'])


def startDetached(command, env=None):
    print(command)
    if sys.platform.find('win') == 0:
        if env:
            # Apply extra env vars for this launch only (cmd /c inherits them).
            parts = []
            for key, value in env.items():
                parts.append('set "%s=%s"' % (key, value))
            parts.append(command)
            command = ' && '.join(parts)
        QtCore.QProcess.startDetached('cmd.exe', ['/c', command])
    else:
        if env:
            exports = ' '.join(
                ['%s="%s"' % (key, value) for key, value in env.items()]
            )
            command = '%s %s' % (exports, command)
        QtCore.QProcess.startDetached('/bin/bash', ['-c', command])


def startBlender():
    startDetached('blender')


def startC4D():
    startDetached('c4d')


def startClarisse():
    startDetached('clarisse')


def startHoudini():
    startDetached('houdini')


def startFusion():
    startDetached('fusion')


def startMaya():
    startDetached('maya')


def startNatron():
    startDetached('natron')


def startNuke():
    startDetached('nuke')


def startNukeX():
    startDetached('nuke --nukex')


def start3DSMax():
    startDetached('3dsmax')


def startSoftimage():
    startDetached('xsi')


def startAfterFX():
    startDetached('afterfx')


def startLightwave():
    startDetached('lightwave')


def getIcon(soft):
    iconpath = cgruutils.getIconFileName(
        os.path.join('software', soft.lower()))
    if iconpath is not None:
        return QtGui.QIcon(iconpath)
    return None


def exampleSoftware(folder, script):
    cmd = os.environ['CGRU_LOCATION']
    cmd = os.path.join(cmd, 'examples')
    cmd = os.path.join(cmd, folder)
    cmd = os.path.join(cmd, script)
    if sys.platform.find('win') == 0:
        cmd += '.cmd'
    else:
        cmd += '.sh'
    print(cmd)
    QtCore.QProcess.startDetached('"%s"' % cmd)


def exampleBlender():
    exampleSoftware('blender', 'start_blender')


def exampleC4D():
    exampleSoftware('Cinema 4D', 'start_c4d')


def exampleClarisse():
    exampleSoftware('clarisse', 'start_clarisse')


def exampleFusion():
    exampleSoftware('Fusion', 'start_fusion')


def exampleHoudini():
    exampleSoftware('houdini', 'start_houdini')


def exampleMaya():
    exampleSoftware('maya', 'start_maya')


def exampleNatron():
    exampleSoftware('natron', 'start_natron')


def exampleNuke():
    exampleSoftware('nuke', 'start_nuke')


def exampleNukeX():
    exampleNuke()


def example3DSMax():
    exampleSoftware('3D Studio Max', 'start_3dsmax')


def exampleSoftimage():
    exampleSoftware('softimage', 'start_softimage')


def exampleAfterFX():
    exampleSoftware('After FX', 'start_afterfx')


def exampleLightwave():
    exampleSoftware('After FX', 'start_lightwave')


def _setupFolder():
    return os.path.join(os.environ['CGRU_LOCATION'], 'software_setup')


def _locateFile(soft):
    name = 'locate_' + soft.lower()
    if sys.platform.find('win') == 0:
        return os.path.join(_setupFolder(), name + '.cmd')
    return os.path.join(_setupFolder(), name + '.sh')


def getDefaultLocation(soft):
    """Return APP_DIR from locate_*.cmd/sh if present."""
    path = _locateFile(soft)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('set APP_DIR='):
                    return line.split('=', 1)[1].strip().strip('"')
                if line.startswith('export APP_DIR='):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception:
        pass
    return None


def writeLocateFile(soft, app_dir, app_exe=None):
    """Write Keeper locate_* file for default interactive launch."""
    setup_file = _locateFile(soft)
    app_dir = os.path.normpath(app_dir)
    if app_exe is None:
        if soft.lower() == 'houdini':
            fx = os.path.join(app_dir, 'bin', 'houdinifx.exe')
            if os.path.isfile(fx):
                app_exe = os.path.join('bin', 'houdinifx.exe')
            else:
                app_exe = os.path.join('bin', 'houdini.exe')
        else:
            app_exe = os.path.basename(app_dir)

    lines = ['Created by Keeper at ' + time.ctime()]
    if sys.platform.find('win') == 0:
        lines[0] = 'rem ' + lines[0]
        lines.append('set APP_DIR=%s' % app_dir)
        lines.append('set APP_EXE=%%APP_DIR%%\\%s' % app_exe)
    else:
        lines[0] = '# ' + lines[0]
        lines.append('export APP_DIR="%s"' % app_dir)
        lines.append('export APP_EXE="${APP_DIR}/%s"' % app_exe)

    with open(setup_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    return setup_file


def locateSoftware(soft):
    filename, fltr = QtWidgets.QFileDialog.getOpenFileName(
        None, 'Select %s executable:' % soft)
    if filename is None:
        return
    filename = str(filename)
    if filename == '':
        return
    filename = os.path.normpath(filename)
    app_dir = os.path.dirname(filename)
    app_exe = os.path.basename(filename)
    if os.path.basename(app_dir) == 'bin':
        app_dir = os.path.dirname(app_dir)
        app_exe = os.path.join('bin', app_exe)
    writeLocateFile(soft, app_dir, app_exe)


def locateBlender():
    locateSoftware('Blender')


def locateC4D():
    locateSoftware('C4D')


def locateClarisse():
    locateSoftware('Clarisse')


def locateFusion():
    locateSoftware('Fusion')


def locateHoudini():
    locateSoftware('Houdini')


def locateMaya():
    locateSoftware('Maya')


def locateNatron():
    locateSoftware('Natron')


def locateNuke():
    locateSoftware('Nuke')


def locateNukeX():
    locateSoftware('NukeX')


def locate3DSMax():
    locateSoftware('3DSMax')


def locateSoftimage():
    locateSoftware('Softimage')


def locateAfterFX():
    locateSoftware('AfterFX')


def locateLightwave():
    locateSoftware('Lightwave')


# ---------------------------------------------------------------------------
# Multi-version discovery / launch (Houdini first; extendable)
# ---------------------------------------------------------------------------

_versions_cache = {}


def discoverHoudiniVersions():
    """Return list of (label, install_path) for installed Houdini builds."""
    if 'Houdini' in _versions_cache:
        return _versions_cache['Houdini']

    versions = []
    if sys.platform.find('win') == 0:
        roots = [r'C:\Program Files\Side Effects Software']
    else:
        roots = ['/opt', '/usr/local']

    for root in roots:
        if not os.path.isdir(root):
            continue
        try:
            names = os.listdir(root)
        except OSError:
            continue
        for name in sorted(names, reverse=True):
            # Windows: "Houdini 21.0.512" ; Linux: "hfs21.0.512"
            is_win = name.startswith('Houdini ') and len(name) > 8 and name[8].isdigit()
            is_linux = name.startswith('hfs') and len(name) > 3 and name[3].isdigit()
            if not (is_win or is_linux):
                continue
            path = os.path.join(root, name)
            versions.append((name, path))

    _versions_cache['Houdini'] = versions
    return versions


def getVersions(soft):
    """Return [(label, path), ...] for softwares that support multi-version."""
    if soft == 'Houdini':
        return discoverHoudiniVersions()
    return []


def startSoftAt(soft, location):
    """Launch software with a specific install location."""
    env = {'HOUDINI_LOCATION': location} if soft == 'Houdini' else None
    if soft == 'Houdini':
        startDetached('houdini', env=env)
    else:
        startDetached(soft.lower())


def setDefaultVersion(soft, location):
    """Set Keeper default version (writes locate_*.cmd)."""
    writeLocateFile(soft, location)
    _versions_cache.pop(soft, None)
    print('Default %s set to: %s' % (soft, location))
