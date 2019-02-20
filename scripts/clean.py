import os
import sys
import glob


def clean_project(root_dir, test=False):
    root_dir = os.path.normpath(root_dir)

    to_clean = glob.glob("{0}/**/*.pyc".format(root_dir), recursive=True)

    for f_path in to_clean:
        print('will delete: ' + f_path)
        if test:
            continue

        os.remove(f_path)

    return to_clean


if __name__ == "__main__":

    root, _ = os.path.split(os.path.split(__file__)[0])

    print('cleaning directory: ' + root)

    if input('continue? y/n \n') not in ['Y', 'y']:
        exit(0)

    if 'clean' in sys.argv or len(sys.argv) == 1:
        clean_project(root)
