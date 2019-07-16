#!/usr/bin/env python3
import os
import subprocess


# TODO: really, I should just change cwd to the directory monitored...
# ...hopefully that'd simplify the arguments taken by various functions....
#... but also, it doesn't really matter lmao


# Persistently check for for new content
def monitor(directory, outfile=None, command=None):

    contents = set(item for item in os.listdir(directory))

    while True:

        new_content = set(item for item in os.listdir(directory) if item not in contents)

        for y in new_content:
            print(y)

            if command:
                run_command(y, directory, command)
            if outfile:
                with open(outfile, "a+") as f:
                    f.write(directory + "/" +  y + "\n")

            #update list of seen content
            contents.add(y)

    return


# Perform shell actions on a given target
def run_command(f, directory, command):

    obj = directory + "/" + f
    if "{x}" in command:
        command = command.replace("{x}", obj)
        subprocess.run(command, shell=True)
    else:
        command = command + " " + obj

    subprocess.run(command, shell=True)

# Persistently check for a certain file
def target_monitor(directory, target, outfile=None, command=None):

    contents = set(item for item in os.listdir(directory))

    while True:

        new_content = set(item for item in os.listdir(directory) if item not in contents)

        for y in new_content:
            if y.startswith(target) or y.endswith(target):
                print(y)

                if command:
                    run_command(y, directory, command)
                if args.outfile:
                    with open(outfile, "a+") as f:
                        f.write(directory + y + "\n")

            #update list of seen content
            contents.add(y)
    return


def main():

    if args.target:
        target_monitor(args.directory, args.target,
                        outfile=args.outfile, command=args.exec)
    else:
        monitor(args.directory, outfile=args.outfile, command=args.exec)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="monitor a directory's contents")

    parser.add_argument("directory", nargs="?", default=".", help="path to directory")
    parser.add_argument("-t", "--target", help="target of monitor")
    parser.add_argument("-x", "--exec",
                        nargs="?",
                        default=None,
                        help="command to execute on contents or target, with {x} as stand in")
    parser.add_argument("-o", "--outfile",
                        default=None,
                        help="output file")

    args = parser.parse_args()

    main()
