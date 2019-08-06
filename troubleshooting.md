# Troubleshooting

Are you getting some error about `ELM-FORMAT NOT FOUND`? Is it giving some unhelpful details about your `PATH`? Here are some recommendations for that case!


## 0. What is a `PATH` variable?

When you run `elm make src/Main.elm`, your computer starts by trying to find a file called `elm`.

The `PATH` is a list of directories to search within. On Mac and Linux, you can see these directories by running:

```
$ echo $PATH
/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/git/bin
```

So running `elm make src/Main.elm` starts by searching the `PATH` for files named `elm`. On my computer, it finds `/usr/local/bin/elm` and then can actually run the command.


## 1. Is `elm-format` installed?

You can install `elm-format` on your computer by running this in your terminal:

```bash
npm install -g elm-format
```

Running this in August 2019 on my Mac, this creates two files:

- `/usr/local/lib/node_modules/elm-format/bin/elm-format` which is the actual executable
- `/usr/local/bin/elm-format` is a symlink to the real executable

The `/usr/local/bin` directory is a very common entry in the `PATH` list, so at this point, it should be possible to run `elm-format` in your terminal. (You may have to restart your terminal!)

This plugin searches the `PATH` for `elm-format` on each run, so it should not be necessary to restart Sublime Text for things to work once it is installed.


## 2. Try adding the `"absolute-path"`?

Go to **Preferences -> Package Settings -> Elm Format on Save -> Settings**

You can now say something like:

```json
{
	"absolute_path": "/usr/local/bin/elm-format"
}
```

The plugin will try to use the exact file that you specify there.

> **Note:** If you have `elm-format` working in your terminal, you can figure out where it lives on Linux and by running:
>
>     $ which elm-format
>     /usr/local/bin/elm-format
>
> That is what it says on my computer, but maybe it will say something else on yours.


## 3. Uninstall `elm-format-on-save`

If none of this works, just uninstall this plugin.

Editor plugins are always breaking because of odd `PATH` variables, operating system details, new versions, etc. Sometimes it's just not worth the time to mess around with this.
