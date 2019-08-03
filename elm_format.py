import os
import os.path
import re
import sublime
import sublime_plugin
import subprocess


class ElmFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        elm_format = find_elm_format()

        if elm_format == None:
            open_panel(self, cannot_find_elm_format_message())
            return

        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        stdout, stderr = subprocess.Popen(
            [elm_format, '--stdin', '--yes', '--elm-version=0.19'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=os.name=="nt").communicate(input=bytes(content, 'UTF-8'))

        if stderr.strip():
            open_panel(self, re.sub('\x1b\[\d{1,2}m', '', stderr.strip().decode()))
        else:
            self.view.replace(edit, region, stdout.decode('UTF-8'))
            self.view.window().destroy_output_panel("elm_format")


class ElmFormatOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        scope = view.scope_name(0)
        if scope.find('source.elm') != -1:
            view.run_command('elm_format')


#
# alternative available in Python 3.3 and up
# shutil.which('elm-format', mode=os.X_OK)
#
def find_elm_format():
    exts = os.environ['PATHEXT'].lower().split(os.pathsep) if os.name == 'nt' else ['']
    for directory in os.environ['PATH'].split(os.pathsep):
        for ext in exts:
            path = os.path.join(directory, 'elm-format' + ext)
            if os.access(path, os.X_OK):
                return path
    return None


def open_panel(self, content):
    window = self.view.window()
    panel = window.create_output_panel("elm_format")
    panel.set_read_only(False)
    panel.run_command('erase_view')
    panel.run_command('append', {'characters': content})
    panel.set_read_only(True)
    window.run_command("show_panel", {"panel": "output.elm_format"})


def cannot_find_elm_format_message():
    return """

I wanted to run `elm-format` but I could not find it!

Your PATH variable led me to check in the following directories:

    TODO
    TODO

But I could not find it in any of them.
"""
