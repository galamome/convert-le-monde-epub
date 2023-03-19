import io
import shutil
import tempfile
import urllib.request
from lxml import etree
import asyncio
import os.path
import aiofiles
import aiohttp

######################################################
# Constants
######################################################


########################################################################
# Functions
########################################################################

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

def convert(nakedFileName):
    # Write file
    epubFileName = f'{nakedFileName}.epub'
    htmlFileName = f'{nakedFileName}.html'
    if not os.path.isfile(epubFileName):
        # Prepare the command to run "pandoc"
        command_to_convert_to_epub = f'pandoc -f html -t epub2 -o {epubFileName} {htmlFileName}'

        return command_to_convert_to_epub
    else:
        print(f'File {epubFileName} already exists, and will NOT be created')
    return ""

##########################################

fileNames = os.listdir('./')

for fileName in fileNames:
    if ".html" in fileName:
        nakedFileName = fileName.split('.')[0]
        command_to_convert_to_epub = convert(nakedFileName)
        # Run the command to run "pandoc"
        asyncio.run(run(command_to_convert_to_epub))