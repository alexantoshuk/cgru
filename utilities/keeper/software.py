# -*- coding: utf-8 -*-
import os
import subprocess
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


def _resolveWrapper(command):
    """Split 'nuke --nukex' -> (absolute path to nuke.cmd, ['--nukex'])."""
    parts = command.split()
    name = parts[0]
    args = parts[1:]
    cgru = os.environ.get('CGRU_LOCATION') or ''
    for candidate in (
        os.path.join(cgru, 'software_setup', 'bin', name + '.cmd'),
        os.path.join(cgru, 'software_setup', 'bin', name),
        os.path.join(cgru, 'bin', name + '.cmd'),
        os.path.join(cgru, 'bin', name),
    ):
        if candidate and os.path.isfile(candidate):
            return candidate, args
    return name, args


def startDetached(command, env=None):
    """Launch a CGRU software wrapper; optional env overrides (e.g. *_LOCATION)."""
    proc_env = os.environ.copy()
    if env:
        for key, value in env.items():
            proc_env[str(key)] = str(value)

    if sys.platform.find('win') == 0:
        wrapper, args = _resolveWrapper(command)
        # Build: cmd /c call "C:\...\houdini.cmd" [--flags]
        # Pass LOCATION via real process env (not `set` in a /c string) so paths
        # with spaces and stale parent LOCATION values work correctly.
        cmdline = ['cmd.exe', '/c', 'call', wrapper] + args
        print('launch:', cmdline, 'env_overrides:', env)
        # CREATE_NO_WINDOW hides the brief console; houdini.cmd uses `start`
        # for the real GUI app. Do not use DETACHED_PROCESS — it often makes
        # the child exit immediately under pythonw/Keeper.
        flags = 0
        if hasattr(subprocess, 'CREATE_NO_WINDOW'):
            flags |= subprocess.CREATE_NO_WINDOW
        subprocess.Popen(cmdline, env=proc_env, creationflags=flags)
    else:
        print(command if not env else '%s  env=%s' % (command, env))
        subprocess.Popen(
            ['/bin/bash', '-c', command],
            env=proc_env,
            start_new_session=True,
        )


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


def _readLocateAppDir(soft):
    """APP_DIR from locate_*.cmd/sh, or None if not set."""
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


def getDefaultLocation(soft):
    """Effective default install path: locate_* if set, else auto-detect (newest)."""
    located = _readLocateAppDir(soft)
    if located:
        return located
    versions = getVersions(soft)
    if versions:
        # discover() sorts newest-first — same idea as setup_*.cmd last dir /b match
        return versions[0][1]
    return None


def _shortVersionLabel(soft, label):
    """'Houdini 21.0.512' -> '21.0.512'; 'Nuke15.0v5' -> '15.0v5'."""
    prefixes = [
        soft,
        'Houdini', 'Maya', 'Nuke', 'Blender', 'Natron', 'Clarisse',
        'Fusion', 'CINEMA 4D', 'Adobe After Effects', 'Softimage',
        'LightWave', 'Lightwave', '3ds Max', '3DSMax',
    ]
    for prefix in prefixes:
        if label.lower().startswith(prefix.lower()):
            rest = label[len(prefix):].lstrip(' _-')
            if rest:
                return rest
    return label


def getDefaultVersionLabel(soft):
    """Short label of effective default, e.g. '21.0.512', or None."""
    loc = getDefaultLocation(soft)
    if not loc:
        return None
    loc_norm = os.path.normpath(loc)
    for label, path in getVersions(soft):
        if os.path.normpath(path) == loc_norm:
            return _shortVersionLabel(soft, label)
    return _shortVersionLabel(soft, os.path.basename(loc))


def writeLocateFile(soft, app_dir, app_exe=None):
    """Write Keeper locate_* file for default interactive launch."""
    setup_file = _locateFile(soft)
    app_dir = os.path.normpath(app_dir)
    if app_exe is None:
        app_exe = _defaultExe(soft, app_dir)

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
# Multi-version discovery / launch (common for all Softwares)
# ---------------------------------------------------------------------------
# Each SoftSpec:
#   env      - LOCATION variable passed into setup_*.cmd when launching a version
#   cmd      - wrapper command from software_setup/bin
#   exe_win / exe_unix - relative executable path inside APP_DIR (for locate_*)
#   scans    - list of scan rules: roots + match(name) -> optional path transform

def _is_win():
    return sys.platform.find('win') == 0


def _prefix_digit(prefix):
    """Match folder names like 'Maya2024', 'Nuke15.0v5', 'Houdini 21.0.512'."""
    plen = len(prefix)

    def match(name):
        if not name.startswith(prefix) or len(name) <= plen:
            return False
        return name[plen].isdigit() or (
            name[plen] == ' ' and len(name) > plen + 1 and name[plen + 1].isdigit()
        )

    return match


def _startswith(prefix):
    return lambda name: name.startswith(prefix)


# Shared scan helpers -------------------------------------------------------

def _scan_children(roots, match, path_of=None):
    """Return [(label, path), ...] for matching child folders under roots."""
    found = []
    seen = set()
    for root in roots:
        if not os.path.isdir(root):
            continue
        try:
            names = os.listdir(root)
        except OSError:
            continue
        for name in sorted(names, reverse=True):
            if not match(name):
                continue
            base = os.path.join(root, name)
            if not os.path.isdir(base):
                continue
            path = path_of(base, name) if path_of else base
            if path is None or not os.path.isdir(path):
                continue
            key = os.path.normcase(os.path.normpath(path))
            if key in seen:
                continue
            seen.add(key)
            found.append((name, path))
    return found


def _houdini_scans():
    if _is_win():
        return _scan_children(
            [r'C:\Program Files\Side Effects Software'],
            _prefix_digit('Houdini'),
        )
    return _scan_children(['/opt', '/usr/local'], _prefix_digit('hfs'))


def _maya_scans():
    if _is_win():
        return _scan_children(
            [r'C:\Program Files\Autodesk'],
            _prefix_digit('Maya'),
        )
    return _scan_children(
        ['/usr/autodesk', '/opt/autodesk', '/usr/local/autodesk'],
        lambda n: n.lower().startswith('maya') and any(ch.isdigit() for ch in n),
    )


def _nuke_scans():
    if _is_win():
        return _scan_children([r'C:\Program Files'], _prefix_digit('Nuke'))
    return _scan_children(
        ['/usr/local', '/opt'],
        lambda n: n.lower().startswith('nuke') and any(ch.isdigit() for ch in n),
    )


def _blender_scans():
    if _is_win():
        return _scan_children(
            [r'C:\Program Files\Blender Foundation'],
            _startswith('Blender'),
        )
    return _scan_children(
        ['/usr/local', '/opt', '/snap'],
        lambda n: n.lower().startswith('blender'),
    )


def _max_scans():
    if not _is_win():
        return []
    return _scan_children(
        [r'C:\Program Files\Autodesk'],
        _startswith('3ds Max'),
    )


def _c4d_scans():
    if _is_win():
        roots = [r'C:\Program Files\MAXON', r'D:\Program Files\MAXON']
    else:
        roots = ['/Applications', '/opt']
    return _scan_children(roots, _startswith('CINEMA 4D'))


def _clarisse_scans():
    if _is_win():
        roots = [r'C:\Program Files\Isotropix']
    else:
        roots = ['/opt', '/usr/local']

    def path_of(base, name):
        nested = os.path.join(base, 'Clarisse')
        return nested if os.path.isdir(nested) else base

    return _scan_children(roots, _startswith('Clarisse'), path_of=path_of)


def _fusion_scans():
    if _is_win():
        return _scan_children(
            [r'C:\Program Files\Blackmagic Design'],
            _startswith('Fusion'),
        )
    return _scan_children(['/opt', '/usr/local'], _startswith('Fusion'))


def _natron_scans():
    if _is_win():
        return _scan_children([r'C:\Program Files\INRIA'], _startswith('Natron'))
    return _scan_children(['/opt', '/usr/local'], _startswith('Natron'))


def _afterfx_scans():
    if not _is_win():
        return _scan_children(
            ['/Applications'],
            _startswith('Adobe After Effects'),
        )

    def path_of(base, name):
        support = os.path.join(base, 'Support Files')
        return support if os.path.isdir(support) else base

    return _scan_children(
        [r'C:\Program Files\Adobe'],
        _startswith('Adobe After Effects'),
        path_of=path_of,
    )


def _softimage_scans():
    if not _is_win():
        return []

    def path_of(base, name):
        app = os.path.join(base, 'Application')
        return app if os.path.isdir(app) else base

    return _scan_children(
        [r'C:\Program Files\Autodesk'],
        _startswith('Softimage'),
        path_of=path_of,
    )


def _lightwave_scans():
    if not _is_win():
        return []
    return _scan_children(
        [r'C:\Program Files\NewTek', r'C:\Program Files\Newtek'],
        _startswith('LightWave'),
    )


# Soft registry: one entry per Names[] item --------------------------------

SOFT_SPECS = {
    'Blender': {
        'env': 'BLENDER_LOCATION',
        'cmd': 'blender',
        'exe_win': 'blender.exe',
        'exe_unix': 'blender',
        'discover': _blender_scans,
    },
    'C4D': {
        'env': 'C4D_LOCATION',
        'cmd': 'c4d',
        'exe_win': 'CINEMA 4D.exe',
        'exe_unix': 'CINEMA 4D',
        'discover': _c4d_scans,
    },
    'Clarisse': {
        'env': 'CLARISSE_LOCATION',
        'cmd': 'clarisse',
        'exe_win': 'clarisse.exe',
        'exe_unix': 'clarisse',
        'discover': _clarisse_scans,
    },
    'Houdini': {
        'env': 'HOUDINI_LOCATION',
        'cmd': 'houdini',
        'exe_win': 'bin\\houdini.exe',
        'exe_unix': 'bin/houdini',
        'discover': _houdini_scans,
    },
    'Maya': {
        'env': 'MAYA_LOCATION',
        'cmd': 'maya',
        'exe_win': 'bin\\maya.exe',
        'exe_unix': 'bin/maya',
        'discover': _maya_scans,
    },
    'Natron': {
        'env': 'NATRON_LOCATION',
        'cmd': 'natron',
        'exe_win': 'bin\\Natron.exe',
        'exe_unix': 'bin/Natron',
        'discover': _natron_scans,
    },
    'Nuke': {
        'env': 'NUKE_LOCATION',
        'cmd': 'nuke',
        'exe_win': None,  # resolved from Nuke*.exe inside folder
        'exe_unix': 'Nuke',
        'discover': _nuke_scans,
    },
    'NukeX': {
        'env': 'NUKE_LOCATION',
        'cmd': 'nuke --nukex',
        'exe_win': None,
        'exe_unix': 'Nuke',
        'discover': _nuke_scans,
    },
    '3DSMax': {
        'env': 'MAX_LOCATION',
        'cmd': '3dsmax',
        'exe_win': '3dsmax.exe',
        'exe_unix': None,
        'discover': _max_scans,
    },
    'Fusion': {
        'env': 'FUSION_LOCATION',
        'cmd': 'fusion',
        'exe_win': 'Fusion.exe',
        'exe_unix': 'Fusion',
        'discover': _fusion_scans,
    },
    'Softimage': {
        'env': 'XSI_LOCATION',
        'cmd': 'xsi',
        'exe_win': 'bin\\XSI.bat',
        'exe_unix': None,
        'discover': _softimage_scans,
    },
    'AfterFX': {
        'env': 'AE_LOCATION',
        'cmd': 'afterfx',
        'exe_win': 'AfterFX.exe',
        'exe_unix': 'After Effects',
        'discover': _afterfx_scans,
    },
    'Lightwave': {
        'env': 'LIGHTWAVE_LOCATION',
        'cmd': 'lightwave',
        'exe_win': 'bin\\Layout.exe',
        'exe_unix': None,
        'discover': _lightwave_scans,
    },
}


_versions_cache = {}


def _defaultExe(soft, app_dir):
    """Pick relative APP_EXE for locate_* based on SoftSpec / folder contents."""
    spec = SOFT_SPECS.get(soft, {})
    if soft == 'Houdini':
        if _is_win():
            for rel in ('bin\\houdinifx.exe', 'bin\\houdini.exe'):
                if os.path.isfile(os.path.join(app_dir, rel)):
                    return rel
            return None
        for rel in ('bin/houdini', 'bin/houdinifx'):
            if os.path.isfile(os.path.join(app_dir, rel)):
                return rel
        return None
    if soft in ('Nuke', 'NukeX') and _is_win():
        # Main launcher looks like Nuke15.0.exe — skip nukeCrashFeedback.exe etc.
        try:
            for name in sorted(os.listdir(app_dir), reverse=True):
                lower = name.lower()
                if not (lower.startswith('nuke') and lower.endswith('.exe')):
                    continue
                if not any(ch.isdigit() for ch in name):
                    continue
                if 'crash' in lower or 'feedback' in lower:
                    continue
                full = os.path.join(app_dir, name)
                if os.path.isfile(full):
                    return name
        except OSError:
            pass
        return None
    key = 'exe_win' if _is_win() else 'exe_unix'
    exe = spec.get(key)
    if exe:
        return exe
    return None


def _installHasExe(soft, app_dir):
    """True if the install folder still contains a launchable executable."""
    if not app_dir or not os.path.isdir(app_dir):
        return False
    rel = _defaultExe(soft, app_dir)
    if not rel:
        return False
    return os.path.isfile(os.path.join(app_dir, rel))


def getVersions(soft):
    """Return [(label, install_path), ...] for installs that still have an exe."""
    if soft in _versions_cache:
        return _versions_cache[soft]
    spec = SOFT_SPECS.get(soft)
    versions = []
    if spec and spec.get('discover'):
        try:
            versions = spec['discover']() or []
        except Exception as err:
            print('Version discover failed for %s: %s' % (soft, err))
            versions = []
    versions = [
        (label, path) for label, path in versions
        if _installHasExe(soft, path)
    ]
    _versions_cache[soft] = versions
    return versions


def startSoftAt(soft, location):
    """Launch software with a specific install location via its LOCATION env."""
    spec = SOFT_SPECS.get(soft)
    if not spec:
        startDetached(soft.lower())
        return
    env = None
    if spec.get('env') and location:
        env = {spec['env']: os.path.normpath(location)}
    startDetached(spec.get('cmd') or soft.lower(), env=env)


def setDefaultVersion(soft, location):
    """Set Keeper default version (writes locate_*.cmd)."""
    writeLocateFile(soft, location)
    # Nuke / NukeX share installs — invalidate both
    _versions_cache.pop(soft, None)
    if soft == 'Nuke':
        _versions_cache.pop('NukeX', None)
    elif soft == 'NukeX':
        _versions_cache.pop('Nuke', None)
    print('Default %s set to: %s' % (soft, location))
