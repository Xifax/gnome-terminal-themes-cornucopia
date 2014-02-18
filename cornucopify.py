#!/usr/bin/env python
#encoding: utf-8
import uuid
import ConfigParser
import os
import cmd
import sys

# init paths and commands
dconf_path = '/org/gnome/terminal/legacy/profiles:'
dconf = os.popen('which dconf').read().strip()
dconf_write = dconf + ' write'
dconf_list = dconf + ' list'
dconf_read = dconf + ' read'
dconf_reset = dconf + ' reset -f '

def get_profile_list():
    """Get existing profiles"""
    # update profile list
    existing_profiles = os.popen(
        '%s /org/gnome/terminal/legacy/profiles:/' % dconf_list
    ).read().split('\n')

    # clean-up profile list
    existing_profiles = map(
        lambda profile: profile.rstrip('/').lstrip(':'),
        existing_profiles
    )
    # list should include uuid only
    existing_profiles = filter(
        lambda profile: len(profile) == 36,
        existing_profiles
    )
    return existing_profiles


def wipe_all_custom_profiles():
    """Will remove all profiles, except for Default"""
    existing_profiles = get_profile_list()
    removed = 0

    for profile in existing_profiles:
        visible_name = os.popen(
            '%s %s/:%s/visible-name' %
            (dconf_read, dconf_path, profile)
        ).read().strip().strip("'")

        # Do not touch default profile
        if visible_name != 'Default':
            remove_profile(profile, existing_profiles)
            removed += 1

    return removed


def remove_profile(profile, existing_profiles):
    """Remove profile and update profile list"""
    os.system(
        '%s "%s/:%s/"' %
        (dconf_reset, dconf_path, profile)
    )

    # update profile list
    existing_profiles.remove(profile)
    profiles = "','".join(existing_profiles)
    os.system(
        "%s %s/list \"['%s']\"" %
        (dconf_write, dconf_path, profiles)
    )


def remove_profiles(theme_name):
    """Remove profiles based on visible name"""
    existing_profiles = get_profile_list()

    removed = 0
    for profile in existing_profiles:
        visible_name = os.popen(
            '%s %s/:%s/visible-name' %
            (dconf_read, dconf_path, profile)
        ).read().strip().strip("'")
        # remove profile, if name matches
        if visible_name == theme_name:
            remove_profile(profile, existing_profiles)
            removed += 1

    return removed


def create_profile(theme_name):
    """Create new profile and update profile list"""
    profile_id = str(uuid.uuid4())
    profile_dir = dconf_path + '/:' + profile_id

    # create new profile
    os.system("%s %s/default \"'%s'\"" % (dconf_write, dconf_path, profile_id))

    # update profile list
    existing_profiles = get_profile_list()
    existing_profiles.append(profile_id)

    profiles = "','".join(existing_profiles)
    os.system(
        "%s %s/list \"['%s']\"" % (dconf_write, dconf_path, profiles)
    )

    # set visible name
    os.system(
        "%s %s/visible-name \"'%s'\"" % (dconf_write, profile_dir, theme_name)
    )

    return profile_id

def write_theme(theme_name, colors):
    """Write single theme profile colors"""
    # create dconf profile
    profile_id = create_profile(theme_name)

    # set color palette
    palette = "', '".join(colors['palette'].split(':'))
    os.system(
        "%s %s/:%s/palette \"['%s']\"" %
        (dconf_write, dconf_path, profile_id, palette)
    )

    # set foreground, background and highlight color
    os.system(
        "%s %s/:%s/bold-color \"'%s'\"" %
        (dconf_write, dconf_path, profile_id, colors['bold'])
    )
    os.system(
        "%s %s/:%s/background-color \"'%s'\"" %
        (dconf_write, dconf_path, profile_id, colors['background'])
    )
    os.system(
        "%s %s/:%s/foreground-color \"'%s'\"" %
        (dconf_write, dconf_path, profile_id, colors['foreground'])
    )

    # make sure the profile is set to not use theme colors
    os.system(
        '%s %s/:%s/use-theme-colors "false"' %
        (dconf_write, dconf_path, profile_id)
    )

    # set highlighted color to be different from foreground color
    os.system(
        '%s %s/:%s/bold-color-same-as-fg "false"' %
        (dconf_write, dconf_path, profile_id)
    )


def get_themes(theme_list='themes'):
    """Get availiable themes and colors from file"""
    themes = {}
    config = ConfigParser.ConfigParser()
    config.read(theme_list)
    for section in config.sections():
        theme = {}
        theme['palette'] = config.get(section, 'palette')
        theme['background'] = config.get(section, 'bg_color')
        theme['foreground'] = config.get(section, 'fg_color')
        theme['bold'] = config.get(section, 'bd_color')
        themes[section] = theme

    return themes


def write_themes(themes):
    """Update configuration using dconf"""
    for theme_name, colors in themes.iteritems():
        write_theme(theme_name, colors)

    return themes


class Cornucopifier(cmd.Cmd):
    """Initialize or remove gnome profiles"""

    def do_write(self, line):
        """Write all themes from ini to gnome profile"""
        themes = write_themes(get_themes())
        print 'Total new themes: %d' % len(themes)

    def do_remove(self, theme):
        """Remove all profiles with the name [theme]"""
        total = remove_profiles(theme)
        print 'Total themes removed: %d' % total

    def do_wipe(self, line):
        """Wipe all custom profiles (Default profile will remain)"""
        total = wipe_all_custom_profiles()
        print 'Total profiles purged: %d' % total

    def do_EOF(self, line):
        """Exit on C^D"""
        return True

    def do_exit(self, line):
        """Quit at once"""
        sys.exit(0)

    def postloop(self):
        """Print newline after each output"""
        print


if __name__ == '__main__':
    Cornucopifier().cmdloop()
