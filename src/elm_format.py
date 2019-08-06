import os
import os.path
import re
import sublime
import sublime_plugin
import subprocess



#### COMMAND ####


class ElmFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        elm_format = find_elm_format(self)

        if elm_format == None:
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



#### ON SAVE ####


class ElmFormatOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        scope = view.scope_name(0)
        if scope.find('source.elm') != -1 and needs_format(self, view.file_name()):
            view.run_command('elm_format')


def needs_format(self, path):
    settings = sublime.load_settings('elm-format-on-save.sublime-settings')
    on_save = settings.get('on_save')

    if isinstance(on_save, bool):
        return on_save

    if isinstance(on_save, dict):
        included = is_included(path)
        excluded = is_excluded(path)
        if isinstance(included, bool) and isinstance(excluded, bool):
            return included and not excluded

    open_panel(self, invalid_settings)
    return False


def is_included(path):
    if including in on_save:
        if not isinstance(on_save.including, list):
            return None

        for string in on_save.including:
            if string in path:
                return True

        return False

    return True


def is_excluded(path):
    if excluding in on_save:
        if not isinstance(on_save.excluding, list):
            return None

        for string in on_save.excluding:
            if string in path:
                return True

        return False

    return False



#### EXPLORE PATH ####


def find_elm_format(self):
    settings = sublime.load_settings('elm-format-on-save.sublime-settings')
    given_path = settings.get('absolute_path')
    if given_path != None and given_path != '':
        if isinstance(given_path, str) and os.path.isabs(given_path) and os.access(given_path, os.X_OK):
            return given_path
        
        open_panel(self, bad_absolute_path)
        return None

    # shutil.which('elm-format', mode=os.X_OK) # only available in Python 3.3
    exts = os.environ['PATHEXT'].lower().split(os.pathsep) if os.name == 'nt' else ['']
    for directory in os.environ['PATH'].split(os.pathsep):
        for ext in exts:
            path = os.path.join(directory, 'elm-format' + ext)
            if os.access(path, os.X_OK):
                return path

    open_panel(self, cannot_find_elm_format())
    return None



#### ERROR MESSAGES ####


def open_panel(self, content):
    window = self.view.window()
    panel = window.create_output_panel("elm_format")
    panel.set_read_only(False)
    panel.run_command('erase_view')
    panel.run_command('append', {'characters': content})
    panel.set_read_only(True)
    window.run_command("show_panel", {"panel": "output.elm_format"})



#### ERROR MESSAGES ####


def cannot_find_elm_format():
    return """-- ELM-FORMAT NOT FOUND -----------------------------------------------

I tried run elm-format, but I could not find it on your computer.

Try the recommendations from:

  https://github.com/evancz/elm-format-on-save/blob/master/troubleshooting.md

If everything fails, just remove the "elm-format-on-save" plugin from
your editor via Package Control. Sometimes it is not worth the trouble.

-----------------------------------------------------------------------

NOTE: Your PATH variable led me to check in the following directories:

    """ + '\n    '.join(os.environ['PATH'].split(os.pathsep)) + """

But I could not find `elm-format` in any of them. Please let me know
at https://github.com/evancz/elm-format-on-save/issues if this does
not seem correct!
"""


invalid_settings = """-- INVALID SETTINGS ---------------------------------------------------

The "on_save" field in your settings is invalid.

For help, check out the section on including/excluding files within:

  https://github.com/evancz/elm-format-on-save/blob/master/README.md

-----------------------------------------------------------------------
"""


bad_absolute_path = """-- INVALID SETTINGS ---------------------------------------------------

The "absolute_path" field in your settings is invalid.

I need the following Python expressions to be True with the given path:

    os.path.isabs(absolute_path)
    os.access(absolute_path, os.X_OK)

Is the path correct? Do you need to run "chmod +x" on the file?

-----------------------------------------------------------------------
"""
