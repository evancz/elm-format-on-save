**NOT PUBLISHED YET / WORK IN PROGRESS**


# Elm Format on Save

Run `elm-format` whenever you save an Elm file.


## Install

0. Install [`elm-format`](https://github.com/avh4/elm-format)
1. Install [`elm-syntax-highlighting`](https://github.com/evancz/elm-syntax-highlighting)
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the Command Palette
3. Select **Package Control: Install Package**
4. Select `elm-format-on-save`

Try saving an Elm file to see if it works. You may see a panel open with troubleshooting advice if something has gone wrong!


## Keyboard Shortcut

You should be able to press `Ctrl+K` `Ctrl+F` (or `Cmd+K` `Cmd+F` on Mac) to run `elm-format` without needing to trigger a save.


## Technical Details

This plugin works by modifying the code in the editor itself.

So when it runs "on save" it is specifically running _before_ the file is saved to disk.

This is really important if you have some elaborate file watching system set up! Other plugins may format _after_ the file is saved to disk, triggering a second save, and thereby degrading the performance of your file watching system. Why compile a file if you are just about to change that file?
