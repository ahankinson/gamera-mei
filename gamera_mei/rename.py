#!/usr/bin/env python

from os.path import *
from os import rename
from sys import argv

def change_content(change_to, dirname, names):
    for name in names:
        full_path = join(dirname, name)
        if isfile(full_path):
            print "Adjusting content in %s" % full_path
            content = open(full_path, "r").read()
            content = content.replace(change_from.capitalize(), change_to.capitalize())
            content = content.replace(change_from.upper(), change_to.upper())
            content = content.replace(change_from, change_to)
            open(full_path, "w").write(content)
        elif isdir(full_path):
            walk(full_path, change_content, change_to)

def rename_files(change_to, dirname, names):
    for name in names:
        full_path = join(dirname, name)
        if isdir(full_path):
            walk(full_path, rename_files, change_to)
        if name.find(change_from) != -1:
            new_name = name.replace(change_from, change_to)
            print "Renaming %s to %s" % (full_path, join(dirname, new_name))
            rename(full_path, join(dirname, new_name))

change_from = 'gamera_mei'
change_to = argv[-1].lower()
print "Changing name of toolkit project to '%s'." % change_to
walk(".", change_content, change_to)
walk(".", rename_files, change_to)
