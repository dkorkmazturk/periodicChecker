# periodicChecker
**periodicChecker** is a Python script to poll a determined webpage within specified intervals for changes. It simply downloads the HTML file of determined webpage and compares it's MD5 hash against the previously taken hash of the same webpage. When it detects a change on a webpage, it prints a message on command line and sends a notification e-mail if e-mail notification function is configured properly.

## Dependencies
* Python >= 3.2

## Usage
`periodicChecker.py <webpage> <period(s|m|h)> (-q)`

## Setting Up E-mail Notifications
You have to uncomment *sendInfoMail* function and other helper lines and set necessary fields in order to get e-mail notifications when a change has determined. Sections needs to be uncommented specified with *# Uncomment this line for e-mail notifications* comments.

## License
This project is licensed under the WTFPL - see the *periodicChecker.py* file for details.
