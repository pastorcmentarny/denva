import subprocess


def clean_all_bins_in_windows():
    cmd = f"rd /s c:\$Recycle.Bin"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ps.communicate()[0]
    return str(result, 'utf-8')



if __name__ == '__main__':
    clean_all_bins_in_windows()