Session Buddy Tool
===========

A simple tool for managing [Session Buddy Chrome Extension][0] data

Features:
* export to JSON
* clear saved sessions
* merge multiple sessions into one


## Requirements
* python
* cjson
* sqllite3

## Setup

Install requiremtents:
```
$ pip install -r requirements.txt
```

## Usage
```
$ ./session_buddy_tool.py -h
usage: session_buddy_tool.py [-h] -a {export,merge,clean} [-e EXCLUDE]
                             [-p PROFILE]

optional arguments:
  -h, --help            show this help message and exit
  -a {export,merge,clean}, --action {export,merge,clean}
                        Action: export, merge, clean
  -e EXCLUDE, --exclude EXCLUDE
                        Path to file with excluded urls
  -p PROFILE, --profile PROFILE
                        Path to Chrome profile

```

[1]: https://chrome.google.com/webstore/detail/session-buddy/edacconmaakjimmfgnblocblbcdcpbko