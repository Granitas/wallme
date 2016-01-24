import subprocess


def set_wallpaper(image_loc):
    subprocess.Popen('feh --bg-fill {}'.format(image_loc), shell=True)
