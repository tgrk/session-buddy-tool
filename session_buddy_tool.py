#!/usr/bin/python
#
# Session Buddy Chrome Extension tool
#
# TODO:
# * update existing item with new 1links collection
# * figure out how to specify excluded urls (file?)
# * check if exists in GetPocket and insert if not
# * find extension db path? what about cross-platform shit?

import sys
import traceback
import argparse
import cjson
import sqlite3
import os
from os.path import expanduser

#
# Helpers
#
def load_exclude_file(path):
    excluded = []
    if os.path.isfile(path):
        with open(path) as f:
            excluded = f.readlines()
    else:
        print "File with excluded urls can not be found!"
    return excluded

def extract_links(row):
    tabs = cjson.decode(row[1])
    row_id = None
    for key in tabs[0].keys():
        obj = tabs[0][key]
        if key == "id":
            row_id = obj
        elif key == "tabs":
            items = []
            for i in obj:
                items.append({"title": i["title"], "url": i["url"]})
    return {"id": row_id, "items": items}

def remove_duplicates(items):
    seen = []
    unique = []
    for item in items:
        if not item["url"] in seen:
            seen.append(item["url"])
            unique.append(item)
    return unique

def filter_excluded(items):
    filtered = []
    for item in items:
        found = 0
        for url in excluded_urls:
            if item["url"].startswith(url):
                found += 1
        if found == 0:
            filtered.append(item)
    return filtered

def get_saved_sessions(conn, table):
    sessions = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, windows FROM %s;" % table)
        for row in cur.fetchall():
            item = extract_links(row)
            sessions += item["items"]

    except sqlite3.Error, e:
        print "Get sessions error: %s" % e.args[0]
    return sessions

def update_row(conn, table, row_id, items):
    return None

def delete_row(conn, table, row_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE * FROM %s WHERE id=?;" % table, row_id)
        return True
    except sqlite3.Error, e:
        print "Delete error: %s" % e.args[0]
        return False
#
# Actions
#
def action_export(conn, tables, excluded_urls):
    items = []
    for table in tables:
        items += get_saved_sessions(conn, table)

    items = filter_excluded(items)
    items = remove_duplicates(items)

    print cjson.encode(items)

def action_merge(conn, tables, excluded_urls):
    return None

def action_clean(conn, tables, excluded_urls):
    try:
        cur = conn.cursor()
        for table in tables:
            cur.execute("DELETE * FROM %s WHERE id=?;" % table)
    except sqlite3.Error, e:
        print "Cleanup error: %s" % e.args[0]

if __name__ == "__main__":
    db_path="%s/.config/google-chrome/Default/databases/chrome-extension_edacconmaakjimmfgnblocblbcdcpbko_0/2" % expanduser("~")
    tables = ["SavedSessions", "PreviousSessions"]

    conn = sqlite3.connect(db_path)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--action",
                            choices=['export', 'merge', 'clean'],
                            help="Action: export, merge, clean", required=True)
        parser.add_argument("-e", "--exclude",
                            help="Path to file with excluded urls")
        args = parser.parse_args()

        excluded_urls = []
        if args.exclude:
            excluded_urls = load_exclude_file(args.exclude)

        if args.action == "export":
            action_export(conn, tables, excluded_urls)
        elif args.action == "clean":
            action_clean(conn, tables, excluded_urls)
        elif args.action == "merge":
            action_merge(conn, tables, excluded_urls)
        else:
            parser.print_help()
            sys.exit(1)

        sys.exit(0)
    except Exception, e:
        print "Main error: %s" % e
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        sys.exit(1)
    finally:
        if conn:
            conn.close()
