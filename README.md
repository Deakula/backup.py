# Backup Script

A simple script to manage local file backups with configurable rotation.

## Usage

### Get Started:

1. Run the script as is with `python3 backup.py` to generate the required directory and file structure.
2. Edit `dirs.txt` by writing the paths to the directories you want to back up, 1 per line, paired with the number of backups of that particular directory you want kept before the oldest is deleted.
   ### For example:
   #### This will create backups for the 3 directories listed retaining 8, 3, and 5 backups of each respectively before deleting the oldest:
   ```py
   /home/[user_name]/pictures, 8
   /home/[user_name]/music, 3
   /home/[user_name]/important files, 5
   ```
3. Run the script with `python3 backup.py` to create a new backup of all the directories you listed in `dirs.txt`

## TODO
- [ ] Add directory compression support.
- [ ] Add support for sending backups offsite.

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
