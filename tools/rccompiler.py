#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Date: Sun Jul 24 20:47:02 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

Assumed Qt related locations of files:
--------------------------------------
.
|-- src
|   `-- qt
|       `--*Design.py
|-- data
|   |-- ui
|   |-- i18n
|   |   `-- *.ts
|   `-- icons
|       |-- flags
|       `-- hicolor
|--tools
|  `--rccompiler.py
|-- projectfile.pro
`-- resourcefile.qrc

Purpose:
--------
One script to rule them all[*]_

.. [*] s/rule them all/compile all resources/g
"""
import os
import sys
import subprocess

from optparse import OptionParser, OptionGroup

description = """rccompiler.py is a utility script for developing PySide
or PyQt4 applications. It automates the process of compiling and updating the
various resources used by the target application.

For PySide development, the script makes use of the following commands:

- pyside-rcc     Used for compiling resources into a python resource file.
                 This is a python wrapper for rcc
- pyside-uic     Used for compiling .ui files and generate python source files.
                 This is a python wrapper for uic-qt4
- pyside-lupdate Used for updating the resources in the project file.
                 This is a python wrapper for lupdate-qt4

For PyQt4 development the following commands is used:

- pyrcc4         Used for compiling resources into a python resource file.
                 This is a python wrapper for rcc
- pyuic4         Used for compiling .ui files and generate python source files.
                 This is a python wrapper for uic-qt4
- pylupdate4     Used for updating the resources in the project file.
                 This is a python wrapper for lupdate-qt4

In addition the script make use of the following Qt4 commands:

- lrelease-qt4    Used to convert xml-based translations ``.ts`` files into
                  compiled ``.qm`` files for use in the Luma application.
"""
(PyQt4, PySide) = range(2)
Binding = PySide
"""Change this to suit your development."""

command = {
    'rcc': ['py-rcc4', 'pyside-rcc'],
    'uic': ['py-uic4', 'pyside-uic'],
    'lupdate': ['py-lupdate4', 'pyside-lupdate'],
    'lrelease-qt4': ['lrelease-qt4', 'lrelease-qt4']}
"""Access commands with command['<key>'][Binding]."""

# --------------------------------------------------------------------------- #
# Filepaths
SRC_ICONS = ['data', 'icons']
SRC_i18n = ['data', 'i18n']
SRC_UI = ['data', 'ui']
DST_i18n = ['data', 'i18n']
DST_UI = ['cconverter', 'qt']

# Files w/filepaths
PROJECT_FILE = ['cconverter.pro']
RESOURCE_FILE = ['cconverter.qrc']
RESOURCE_PYFILE = ['cconverter', 'qt', 'resources.py']


class ProjectFile(object):
    """Object respresenting the project file.

    The sections in the project file is represeneted as a python dict,
    with a string as key, and a list of strings as value::

        pro = {
            section1 : [item, item, ...],
            section2 : [item,  ...],
            ...
        }

    where section can be SOURCES, FORMS, TRANSLATIONS, etc.
    The project file will thus be transformed to::

        ...

        section1 += item
        section1 += item
        section1 += ...

        section2 += item
        section2 += ...

        ...
    """
    def __init__(self):
        self.proDict = {}
        self.proDict['CONFIG'] = ['qt debug']
        self.proDict['RESOURCES'] = ['/'.join(RESOURCE_PYFILE)]

    def __str__(self):
        """Retruns the string representation of the project file."""
        return '\n'.join([line for line in self.asList()])

    @staticmethod
    def targetFile():
        return PROJECT_FILE[-1]

    def addItem(self, section, item):
        """Adds a correctly formatted section entry to the data
        structure.

        :param section: the section for `item`
        :type section: string
        :param item: the item to include. should include the path
         relative to the project file.
        :type item: string
        """
        if section in self.proDict:
            self.proDict.get(section).append(item)
        else:
            self.proDict[section] = [item]

    def update(self):
        """Uses `self.find` to locate all the files to include. Should
        be called before `self.save`.
        """
        self.find(section='SOURCES', path=getPath(['cconverter', 'qt']),
                  extension='.py', ignore=['__init__.py'])
        self.find(section='FORMS', path=getPath(SRC_UI),
                  extension='.ui')
        self.find(section='TRANSLATIONS', path=getPath(SRC_i18n),
                  extension='.ts')

    def find(self, section, path, extension='', ignore=[]):
        """Locates the files that should be included in the project
        file.

        :param section: the file section, i.e. SOURCES, TRANSLATIONS
         FORMS, etc. (see: ??)
        :type section: string
        :param path: the path to look inside. Both relative and
         absolute path is supported.
        :type path: string
        :param extension: the file extension of the files to include.
        :type extension: string
        :param ignore: a list of files to ignore.
        :type ignore: list
        """
        if verbose:
            print '[{0}]'.format(section)
        cwd = os.getcwd() + os.sep
        for p, dirs, files in os.walk(path):
            if p.endswith('rejects'):
                continue

            for file in files:
                relpath = p.replace(cwd, '').replace('\\', '/')
                if not file in ignore and file.endswith(extension):
                    file = os.path.join(relpath, file)
                    self.addItem(section, file)
                    if verbose:
                        print '  {0}'.format(file)

    def save(self):
        """Saves the contens of `self.proDict` to disk. Uses the format
        returned from `self.__str__`.
        """
        with open(ProjectFile.targetFile(), 'w') as f:
            f.write(str(self))
            f.write('\n')

    def asList(self):
        """Returns the project file as a list of lines."""
        proFile = []
        for section, items in sorted(self.proDict.iteritems()):
            for item in items:
                line = '{0} += {1}'
                proFile.append(line.format(section, item))

            proFile.append('')

        return proFile


class ResourceFile(object):
    """Object representing the resource file.

    The main part of the resource file is represented as a python dict,
    with a string as key, and a tuple containg the accesiable alias and
    the location of the resource::

        qrc = {
            prefix : (alias, location),
            prefix : (alias, location),
            ...,
        }

    which will then be transformed to::

        <!DOCTYPE RCC><RCC version="1.0">
          <qresource prefix="prefix">
            <file alias="alias">location/name</file>
          </qresource>
          <qresource prefix="prefix">
            <file alias="alias">location/name</file>
          </qresource>
          ...
        </RCC>
    """
    header = '<!DOCTYPE RCC><RCC version="1.0">'
    """default .qrc header definition."""
    footer = '</RCC>'
    """default .qrc footer definition."""

    def __init__(self, resourceRoot):
        """Initializes a `LumaQrc` object.

        :param resourceRoot: the resource root location (relative to
         the repository root and location of the resource file)
        :type resourceRoot: string
        """
        self.root = resourceRoot
        self.qrcDict = {}
        self.qrcFile = []

    def __str__(self):
        """Returns the .qrc file as a string. The ``newline`` character
        is added after each line.
        """
        return '\n'.join([line for line in self.asList()])

    @staticmethod
    def targetFile():
        return RESOURCE_FILE[-1]

    def getIconPrefix(self, path):
        """All we need to do for the icontheme paths is to look for the
        size folder. This is done by splitting the folder items on 'x'
        and see if the first item ``isdigit``.

        Returns a prefix containing the path folders preceeding the
        size folder, including the size folder (without 'xSize').

        :param path: the path to get the 'prefix' from.
        :type path: string
        """
        list = path.split(os.sep)
        for item in list:
            tmp = item.split('x')
            if tmp[0].isdigit():
                return 'icons/{0}'.format(tmp[0])

            # A special case for the ``scalable`` directory
            if item == 'scalable':
                return 'icons/svg/'

        # If we end up here we simple return ``icons`` as the prefix
        return 'icons'

    def addResource(self, prefix, path, file):
        """Adds or appends a resource to the value for key `prefix`.
        The alias for the resource will be the resource filename
        without the filending, i.e.::

            ``help.png`` gets the alias ``help``

        :param prefix: the prefix is the accessor root for the resource
         and is typically ``icons`` or ``i18n``.
        :type prefix: string
        :param path: the realtive path to the resource, not including
         the filename.
        :type path: string
        :param file: the resource filename, by which the alias is
         created.
        :type file: string
        """
        if prefix == 'icons':
            prefix = self.getIconPrefix(path)
            alias = file[:-4]
        else:
            alias = file[:-3].replace('cconverter_', '')

        if prefix in self.qrcDict:
            self.qrcDict.get(prefix).extend([(alias, path, file)])
        else:
            self.qrcDict[prefix] = [(alias, path, file)]

    def update(self):
        """Scannes the ``resources`` directory for resources to include
        in the resource file.

        We look for translation files and icons.
        """
        for path, dirs, files in os.walk(self.root):
            for file in sorted(files):
                if path.endswith('i18n') and file[-3:] == '.qm':
                    self.addResource('i18n', path, file)
                elif file[-4:] in ['.png', '.gif']:
                    self.addResource('icons', path, file)

    def save(self):
        """Saves the resource file to disk.
        """
        with open(ResourceFile.targetFile(), 'w') as f:
            f.write(str(self))
            f.write('\n')

    def asList(self, indentation=2):
        """Returns the .qrc file as a list of lines. By default the
        lines in the list is indented with 2 spaces.

        :param indentation: an integer defining how many spaces to use for
         indentation. Use 0 for no indentation (default is 2).
        :type indentation: int
        """
        indent = ''
        for i in xrange(indentation):
            indent = ' {0}'.format(indent)

        self.qrcFile.append(ResourceFile.header)
        for prefix, values in self.qrcDict.iteritems():
            line = '{0}<qresource prefix="{1}">'
            self.qrcFile.append(line.format(indent, prefix))
            for v in values:
                line = '{0}{0}<file alias="{1}">{2}/{3}</file>'
                self.qrcFile.append(line.format(indent, v[0], v[1], v[2]))

            self.qrcFile.append('{0}</qresource>'.format(indent))

        self.qrcFile.append(ResourceFile.footer)
        return self.qrcFile


def run(cmd, args=[]):
    """Executes the command `cmd` with optional arguments `args`,
    provided it is available on the system.

    Parameters:

    - `cmd`: The program command.
    - `args`: a list of arguments to pass to `cmd` (default is []).
    """
    if not dryrun:
        args.insert(0, cmd)
        proc = subprocess.Popen(args, shell=False, stderr=sys.stderr)
        retval = proc.wait()
        return retval


def writeToDisk(content, where):
    """Writes the `list` to disk, item for item.

    :param content: the content to write to disk.
    :type content: list
    :param where: the path to file we're writing to.
    :type where: string
    """
    if verbose:
        print 'Writing content to {0}'.format(where)

    if not dryrun:
        with open(where, 'w') as f:
            f.write('\n'.join([line for line in content]))


def getPath(dirList):
    """Ensures that we get correct paths. That is we change our
    working directory to the top-level (one step up from tools).

    Returns a cross-platform filepath from file system root including
    the last directory in the path list.

    :param dirList: a list of directories to join from cwd.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == 'tools':
        os.chdir(os.path.split(cwd)[0])

    path = os.getcwd()

    for dir in dirList:
        path = os.path.join(path, dir)

    return path


def compileResources():
    """Compiles the resources defined in the resource file into the
    `RESOURCE_PYFILE` file.
    """
    _qrc = getPath(RESOURCE_FILE)
    _rc = getPath(RESOURCE_PYFILE)

    cmd = command['rcc'][Binding]
    if sys.platform.lower().startswith('win'):
        cmd = '{0}.exe'.format(cmd)

    args = [_qrc, '-py2', '-o', _rc]

    if verbose:
        print 'Compiling resources:'
        print '  source file: {0}'.format(_qrc)
        print '  target file: {0}'.format(_rc)
        print 'Executing:'
        print '  {0} {1}'.format(cmd, ' '.join([arg for arg in args]))

    run(cmd, args)


def compileUiFiles(all=False):
    """Displayes a list of all *.ui files, and prompts for a index
    based selection. The selected file(s) is then compiled to python
    code.

    Parameters:

    - `all`: a boolean value indicating wether or not we are to compile
      all *.ui files we find or compile a selection. If the script is
      run with the ``-f`` option `all` should be ``True``. We also use
      this value to determine if we print the slection list. (default
      is ``False``)
    """
    selection = {}
    uifiles = []

    # If `all`is True we do not print anything related to the selection
    # list.
    if not all:
        print 'Available *.ui files:'
        print

    index = 1
    for path, dirs, files in os.walk(getPath(SRC_UI)):
        if files != []:
            basename = os.path.basename(path)
        for file in files:
            if not file.endswith('.ui'):
                continue
            selection[index] = os.path.join(path, file)
            if not all:
                print '  {0:2d} {1}'.format(index, file)

            index += 1

    # If all is False we prompt for the index of the file(s) to compile
    compile = []
    if all:
        compile = selection.values()
    else:
        input = raw_input('\nEnter the index of the file(s) to compile\n' +
                          '(use * to compile all files listed):')

        nums = input.split(' ')
        if '*' in nums:
            compile = selection.values()
        else:
            for n in nums:
                if n.isdigit():
                    compile.append(selection[int(n)])

    # Iterate through the file(s) marked for compiling, and run
    # the *pyuic4* command.
    cmd = command['uic'][Binding]
    if sys.platform.lower().startswith('win'):
        cmd = '{0}.bat'.format(cmd)

    if verbose:
        print 'Compiling ui files:'

    for file in compile:
        basename = os.path.basename('{0}.py'.format(file[:-3]))
        path = getPath(DST_UI)

        target = os.path.join(path, basename)
        args = [file, '-o', target]

        if verbose:
            print '  Ui file: {0}'.format(file)
            print '  Target file: {0}'.format(target)
            print

        if not dryrun:
            run(cmd, args)


def updateTranslationFiles():
    """Just executes the ``pylupdate4`` command on the ``luma.pro``
    file.
    """
    # FIXME: Might want to extend this utility some more, with options
    #        for generating new translation files (skeletons that is).
    lumapro = ProjectFile.targetFile()
    cmd = command['lupdate'][Binding]

    if sys.platform.lower().startswith('win'):
        cmd = '{0}.exe'.format(cmd)

    args = ['-noobsolete']

    if verbose:
        args.extend(['-verbose', lumapro])
        print 'Updating translation files...'
        print '  Project file: {0}'.format(lumapro)
        print cmd, ' '.join([a for a in args])
    else:
        args.append(lumapro)

    if not dryrun:
        run(cmd, args)


def compileTranslationFiles():
    """Runs lrelease-qt4 on the project file, in order to create
    compiled ``.qm`` files from the ``.ts`` translation files.
    """
    _pro = ProjectFile.targetFile()
    cmd = command['lrelease'][Binding]
    args = ['-noobsolete']

    if sys.platform.lower().startswith('win'):
        cmd = '{0}.exe'.format(cmd)

    if verbose:
        args.append(['-verbose', _pro])
        print 'Compiling translation files...'
        print '  Project file: {0}'.format(_pro)
        print cmd, ' '.join([a for a in args])
    else:
        args.append(_pro)

    if not dryrun:
        run(cmd, args)


def updateResourceFile():
    """Updates the resource file and writes the content to disk.
    """
    qrc = ResourceFile(resourceRoot='data')
    if verbose:
        print 'Updating resource file...'
        print '  Target file: {0}'.format(qrc.targetFile())
        print '  Scanning for resources...'
    qrc.update()
    if verbose:
        print '  Saving resource file...'
        print
    if not dryrun:
        qrc.save()


def updateProjectFile():
    """Updates the project file and writes the content to disk.
    """
    pro = ProjectFile()
    if verbose:
        print 'Updating project file:'.format(pro.targetFile())
        print '  Looking for files to include...'
    pro.update()
    if verbose:
        print '  Saving project file...'
        print
    if not dryrun:
        pro.save()


def main():
    """Sets up the option parser, parsers the commandline for opations
    and arguments, and runs the appropriate methods.
    """
    global verbose, dryrun

    usage = '%prog [options]'
    # Main Options:
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-f', '--full-run',
        dest='full_run', action='store_true',
        help='Do a full run. This involves first compiling all ui files, ' +
        'creating the .qrc file, generate the resource.py file, update ' +
        'translation files, and update the project file.'
    )
    parser.add_option(
        '-u', '--compile-ui-files',
        dest='ui_files', action='store_true',
        help='List all .ui files, and choose the one [or all] files to compile'
    )
    parser.add_option(
        '-q', '--update-qrc',
        dest='qrc_file', action='store_true',
        help='Create and write the .qrc file to disk'
    )
    parser.add_option(
        '-t', '--update-ts',
        dest='ts_files', action='store_true',
        help='Creates or updates the application translations files. ' +
        'This is done by reading the project file. (NOTE: the .ts files, ' +
        'obviously, needs to be updated manually with QLinguist afterwards).'
    )
    parser.add_option(
        '-p', '--update-pro',
        dest='pro_file', action='store_true',
        help='Creates or updates the application project file.'
    )
    # Debug Options:
    group = OptionGroup(parser, 'Debug Options')
    group.add_option(
        '-d', '--dry',
        dest='dry', action='store_true',
        help='Do a dry-run to see what will be done, without doing anything ' +
        '(NOTE: verbose will be set to True when this option is enabled.'
    )
    group.add_option(
        '-v', '--verbose',
        dest='verbose', action='store_true',
        help='Show output and information on whats going on'
    )
    group.add_option(
        '-i', '--info',
        dest='info', action='store_true',
        help='Show script information'
    )
    parser.add_option_group(group)

    (opt, args) = parser.parse_args()

    verbose = opt.verbose
    dryrun = opt.dry

    if dryrun:
        verbose = True

    if opt.info:
        print short_description
        parser.print_usage()
        print description
        sys.exit()

    if dryrun:
        print u'!!!!!!!!!!!!!!!\n!!! DRY-RUN !!!\n!!!!!!!!!!!!!!!'

    if len(sys.argv) == 1:
        print description
        parser.print_help()

    if opt.full_run:
        updateResourceFile()
        updateTranslationFiles()
        updateProjectFile()
        compileResources()
        compileUiFiles(all=True)
        sys.exit()

    if opt.qrc_file:
        updateResourceFile()
        compileResources()

    if opt.ui_files:
        compileUiFiles(all=False)

    if opt.ts_files:
        updateTranslationFiles()

    if opt.pro_file:
        updateProjectFile()


if __name__ == '__main__':
    """We first ensures that we change our working directory to the
    repository root. That is, if the script is beeing invoked from the
    ``tools`` folder, we change directory one level up.

    .. warning::
       The script will fail if beeing invoked from a directory deeper
       than the tools folder, i.e. python ../../rccompiler.py
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == u'tools':
        os.chdir(os.path.split(cwd)[0])

    sys.exit(main())


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
