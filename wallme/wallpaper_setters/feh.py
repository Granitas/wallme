import subprocess

ABS_FEH = subprocess.check_output(['which', 'feh']).decode('utf-8').strip()


def set_wallpaper(image_loc):
    subprocess.Popen('{} --bg-fill {}'.format(ABS_FEH, image_loc), shell=True)
