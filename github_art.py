import sys
import datetime
import subprocess

EDIT_FILE = 'edit.txt'  # the file that will be updated
COLORED = '#'           # colored mark

WIDTH = 52
HEIGHT = 7

def main():

    if len(sys.argv) < 2:
        print("[*] Usage: python %s <art_file_name>", sys.argv[0])
        exit()

    # open pixel art file
    try:
        art = open(sys.argv[1], 'r').read().split()
    except FileNotFoundError:
        print("[-] %s not exists...", sys.argv[1])
        exit()

    # check pixel art format
    if len(art) != HEIGHT:
        print("[-] File format wrong, it must be [52x7]")
        exit()
    for p in art:
        if len(p) != WIDTH:
            print("[-] File format wrong, it must be [52x7]")
            exit()

    current_day = datetime.date.today()
    contrib_weeks = 52
    contrib_days = (current_day.weekday() + 1) % 7

    # first day that is shown on contribution graph
    start_day = current_day - datetime.timedelta(weeks=contrib_weeks, days=contrib_days)

    columns = zip(*art)

    # start drawing
    subprocess.call(['git', 'init'])

    cnt = 0
    for col in columns:
        for pixel in col:

            if pixel == COLORED:
                with open(EDIT_FILE, 'w') as f:
                    f.write(str(cnt))

                update_day = (start_day + datetime.timedelta(days=cnt)).ctime()
                subprocess.call(['git', 'add', '-A'])
                subprocess.call(['git', 'commit', '-am', '"update"', '--date', update_day])

            cnt += 1

    print("Done")

if __name__ == '__main__':
    main()
