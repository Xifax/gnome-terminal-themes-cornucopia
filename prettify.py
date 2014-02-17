import uuid
import ConfigParser
import os

dconf_path = '/org/gnome/terminal/legacy/profiles:'
# TODO: get dconf as env variable?
dconf = 'dconf'

def create_profile(theme_name):
    """Create new profile and update profile list"""
    profile_id = str(uuid.uuid4())
    profile_dir = dconf_path + '/:' + profile_id

    # create new profile
    os.system("dconf write %s/default \"'%s'\"" % (dconf_path, profile_id))

    # update profile list
    existing_profiles = os.popen(
        'dconf list /org/gnome/terminal/legacy/profiles:/'
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
    existing_profiles.append(profile_id)

    profiles = "','".join(existing_profiles)
    os.system(
        "dconf write %s/list \"['%s']\"" % (dconf_path, profiles)
    )

    # set visible name
    os.system(
        "dconf write %s/visible-name \"'%s'\"" % (profile_dir, theme_name)
    )

    return profile_id

def write_theme(theme_name, colors):
    """Write single theme profile colors"""
    # create dconf profile
    profile_id = create_profile(theme_name)

    # set color palette
    palette = "', '".join(colors['palette'].split(':'))
    os.system(
        "dconf write %s/:%s/palette \"['%s']\"" %
        (dconf_path, profile_id, palette)
    )

    # set foreground, background and highlight color
    os.system(
        "%s write %s/:%s/bold-color \"'%s'\"" %
        (dconf, dconf_path, profile_id, colors['bold'])
    )
    os.system(
        "%s write %s/:%s/background-color \"'%s'\"" %
        (dconf, dconf_path, profile_id, colors['background'])
    )
    os.system(
        "%s write %s/:%s/foreground-color \"'%s'\"" %
        (dconf, dconf_path, profile_id, colors['foreground'])
    )

    # make sure the profile is set to not use theme colors
    os.system(
        '%s write %s/:%s/use-theme-colors "false"' %
        (dconf, dconf_path, profile_id)
    )

    # set highlighted color to be different from foreground color
    os.system(
        '%s write %s/:%s/bold-color-same-as-fg "false"' %
        (dconf, dconf_path, profile_id)
    )


def get_themes(theme_list='themes'):
    """Get availiable themes and colors from file"""
    themes = {}
    config = ConfigParser.ConfigParser()
    config.read(theme_list)
    for section in config.sections():
        theme = {}
        theme['palette'] = config.get(section, 'palette').strip('"')
        theme['background'] = config.get(section, 'bg_color').strip('"')
        theme['foreground'] = config.get(section, 'fg_color').strip('"')
        theme['bold'] = config.get(section, 'bd_color').strip('"')
        themes[section] = theme

    return themes


def write_themes(themes):
    """Update configuration using dconf"""
    for theme_name, colors in themes.iteritems():
        write_theme(theme_name, colors)


# TODO: include function batch remove profiles by name (not by id)
if __name__ == '__main__':
    write_themes(get_themes())
