# Gnome terminal theme compilation

tl;dr
-----

Python script to batch-create multiple profiles for new gnome terminal using
dconf, based on ini specifications. Many themes included.

Why
---

After much deliberation, the only theme for Gnome3.8 Terminal I could install
without excruciating pains and casual torture was the infamous Solarized theme.
So, let's port some of the existing themes for dconf, i.e., new gnome terminal.
And while we are at it, let's include conversions of various themes from iTerm
and so on.

Basic idea
----------

Save every theme in large ini file, theme is defined by for params:

- foreground color;
- background color;
- bold color;
- theme color palette.

The whole procedure consists of translating those themes into dconf profiles:

- creating new profile with unique id (otherwise, it won't work at all);
- updating list of active profiles, including new ones;
- setting profile variables based on ini file contents.

And voilà, we've got ourselves gnome terminal with a whole load of themes!
Probably much more than we originally wanted...

Additional functionality
------------------------

You may also batch-remove profiles based on theme name and wipe all
non-default profiles.

Notes
-----

* Python2 is used as language of choice, python3 won't work;
* No additional python libs required;
* All commands are executed from simple cmd shell;
* I own none of the provided themes. Bless their authors, yada-yada.

Themes included:
---------------

Mostly dark ones:

* Molokai
* Monokai
* Monokai soda
* Smyk
* Solarized
* Tomorrow
* Dracula
* Misterioso
* Obdisidian
* Chalkboard
* Github
* Espresso

todo
----

Link all those themes to corresponding web pages, add more themes, refactor,
shave yaks, etc. Tool to convert various existing theme configs to ini would be
nice too.
