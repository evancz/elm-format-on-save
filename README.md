**NOT PUBLISHED YET / WORK IN PROGRESS**


# Elm Format on Save

Run `elm-format` whenever you save an Elm file.

And add the keyboard shortcut `Ctrl+K` `Ctrl+F` (or `Cmd+K` `Cmd+F` on Mac) to run `elm-format` any time you want. No need to save.


## Install

0. Install [`elm-format`](https://github.com/avh4/elm-format)
1. Install [`elm-syntax-highlighting`](https://github.com/evancz/elm-syntax-highlighting)
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the Command Palette
3. Select **Package Control: Install Package**
4. Select `elm-format-on-save`

Try saving an Elm file to see if it works. You may see a panel open with troubleshooting advice if something has gone wrong!


## Including/Excluding Files

Do you only want `elm-format` to run on certain files? (e.g. only work code)

Go to **Preferences -> Package Settings -> Elm Format on Save -> Settings**

You will see two panels. The left is all the defaults and the right is your custom overrides. So in the right panel, you can override the default settings with something like:

```json
{
    "on_save": {
        "including": ["my/company/"],
        "excluding": ["src/generated/"]
    }
}
```

This would mean that you only run `elm-format` on code that is in the `my/company/` directory, but you skip any files in the `src/generated` directory.

See the left settings panel for more information about how to include and exclude files!


## Technical Details

This plugin works by modifying the code in the editor itself.

So when it runs "on save" it is specifically running _before_ the file is saved to disk.

This is really important if you have some elaborate file watching system set up! Other plugins may format _after_ the file is saved to disk, triggering a second save, and thereby degrading the performance of your file watching system. Why compile a file if you are just about to change that file?
