#!/usr/bin/python3

from datetime import datetime
import json
from os import makedirs, path as p, getcwd
from shutil import copytree, rmtree
from logging import basicConfig, info, error, INFO

CWD = p.dirname(p.abspath(__file__))


def get_dest(dest: str, dir_name: str) -> str:
    return p.join(
        dest,
        "{0}_{1}".format(
            str(datetime.now().strftime(
                f"%Y-%m-%d_%H-%M-%S-%f"
            )).split('.')[0],
            dir_name
        )
    )


def get_abs(path: str) -> str:
    return p.join(CWD, path)


def main():
    if not p.exists(get_abs("output.log")):
        open(get_abs("output.log"), 'w+').close()

    basicConfig(
        filename=get_abs("output.log"),
        encoding='utf-8',
        level=INFO
    )

    if not p.exists(get_abs("dirs.txt")):
        info(
            "Directory list file 'dirs.txt' does" +
            " not exist. Creating it..."
        )

        open(get_abs("dirs.txt"), 'w+').close()

        info(
            "Directory list file 'dirs.txt' created." +
            " Please add the full paths of the directories" +
            " to it that you want backed up."
        )

    if not p.exists(get_abs("backups")):
        info("Backups directory does not exist. Creating it...")
        makedirs(get_abs("backups"))
        with open(get_abs("backups/DO NOT EDIT DIRECTORY CONTENTS MANUALLY"), 'w') as fi:
            fi.write("DO NOT EDIT DIRECTORY CONTENTS MANUALLY")

    with open(get_abs("dirs.txt")) as fi:
        for src_amt in fi.readlines():
            try:
                source = p.normpath(src_amt.split(',')[0])

                if not p.isdir(source):
                    raise NotADirectoryError(source)

                max = int(
                    src_amt.split(',')[1].replace(' ', '').replace(
                        '\n', ''
                    )
                )

                dir_name = p.basename(source)
                dest = p.join(get_abs("backups"), dir_name)
                new_name = get_dest(dest, dir_name)
                config_path = p.join(dest, "config.json")

                backups = []

                if not p.exists(dest):
                    makedirs(dest)

                    with open(p.join(dest, config_path), 'w+') as fi:
                        json.dump({'backups': []}, fi, indent=4)
                else:
                    with open(p.join(dest, config_path)) as fi:
                        data: dict[str, list[str] | None] = (
                            json.loads(fi.read())
                        )
                        backups = list(data['backups'])

                for backup in backups:
                    if not p.exists(backup):
                        backups.remove(backup)

                info(f"Attempting to backup '{source}'...")

                if len(backups) == max:
                    info(
                        f"Backup folder for {dir_name} is full." +
                        " Removing oldest backup and shifting the rest..."
                    )
                    rmtree(backups.pop(0))

                info(
                    "Copying '{0}' to '{1}'...".format(
                        source,
                        new_name,
                    )
                )

                copytree(source, new_name)

                backups.append(new_name)

                with open(p.join(dest, config_path), 'w') as fi:
                    json.dump({'backups': backups}, fi, indent=4)

            except Exception as err:
                error(err)


if __name__ == "__main__":
    main()
