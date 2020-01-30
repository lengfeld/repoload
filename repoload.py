#!/usr/bin/env python3
#
# Copyright 2019 David Zerulla and Stefan Lengfeld
#
# SPDX-License-Identifier: MIT

"""
Query gerrit and download a selected CR or crossrepo topic with repo.
"""

import argparse
import subprocess
import sys
import json
import os

__VERSION__ = "0.1"

# TODO Get this url from the manifest repo at the path '.repo/manifests.git/'.
# This will mostly be the correct gerrit server url. Overwriting by a
# enviornment variable should be only the fallback.
# TODO if a environment variable is used, allow some sort of directory
# selection.  Maybe the user has multiple repo checkouts from different gerrit
# servers.
try:
    URL = os.environ['GERRIT_URL']
except KeyError:
    print("Set environment variable GERRIT_URL.", file=sys.stderr)
    sys.exit(1)


# Global Flags
DEBUG = False


# Gerrit documentation
#   https://gerrit-review.googlesource.com/Documentation/cmd-query.html
#   https://gerrit-review.googlesource.com/Documentation/user-search.html
#   https://gerrit-review.googlesource.com/Documentation/json.html
def query(url, query):
    # TODO Make port configurable
    cmd = "ssh -p 29418 {} gerrit query --format=JSON '{}'".format(url, query)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    if p.returncode != 0:
        raise Exception("Error while executing: {}".format(cmd))

    # Output is a '\n'-separate list of json strings
    lines = stdout.split(b'\n')

    # The output is terminator semantics, so the last element after the split
    # is empty.  Remove it.
    assert(len(lines) >= 1 and len(lines[-1]) == 0)
    del lines[-1]

    # JSON is UTF8 by specification
    jsons = [json.loads(line.decode("utf8")) for line in lines]

    if DEBUG:
        print("Query:", cmd, file=sys.stderr)
        print("Response:\n", "\n".join(str(j) for j in jsons), file=sys.stderr)

    # The last line/JSON object is a special query result object
    #   {'runTimeMilliseconds': 28, 'moreChanges': False, 'rowCount': 74, 'type': 'stats'}
    # Return it separately, because it does not belong logical to the query
    # result.
    assert(jsons[-1].get("type") == 'stats')

    # TODO Implement gerrits pagination
    if jsons[-1].get("moreChanges"):
        raise Exception("Gerrit's ppagination not implemented. Send patches.")

    return jsons[:-1], jsons[-1]


def print_open_changes(args):
    json_crs, _ = query(URL, "is:open")
    for cr in sorted(json_crs, key=lambda cr: cr.get('number')):
        author = "%s <%s>" % (cr.get('owner').get('name'), cr.get('owner').get('email'))
        topic = cr.get('topic')
        if topic is not None:
            topic_str = " [topic: %s]" % (topic,)
        else:
            topic_str = ""
        print("%d: %s (%s)%s" % (cr.get('number'), cr.get('subject'), author, topic_str))
    return 0


def print_open_topics(args):
    # Query all open Change Request. There is no API to retrieve a list of
    # topics directly.
    json_crs, _ = query(URL, "is:open")

    # Some Change Requests do not have a topic, filter these out.
    json_crs = [cr for cr in json_crs if cr.get("topic") is not None]

    # Reduce duplicate elements in the topic list.
    # Create a map/dict with key 'topic name' and value list of change requests
    topics = {}
    for cr in json_crs:
        try:
            topics[cr.get("topic")].append(cr)
        except KeyError:
            topics[cr.get("topic")] = [cr]

    for topic in sorted(topics.keys()):
        authors = sorted(set(cr.get("owner").get("name") for cr in topics[topic]))
        print("%s (%s)" % (topic, ", ".join(authors)))
    return 0


def get_changes_for_topic(topic):
    changes, _ = query(URL, "topic:'%s' is:open" % (topic,))
    return changes


def get_change(number):
    changes, _ = query(URL, "%s" % (number,))
    if len(changes) != 1:
        raise Exception("Cannot find change for id %s" % (number,))
    return changes[0]


def download(args):
    dry_run = args.dry_run

    number_or_string = args.value
    if number_or_string.isdigit():
        # Caller has given a CR number
        changes = [get_change(number_or_string)]
    else:
        # Caller has given a topic name
        topic = number_or_string
        changes = get_changes_for_topic(topic)

    # Make the order of download deterministic
    changes.sort(key=lambda change: change.get("project"))

    for change in changes:
        download_change(change, dry_run)
    return 0


def download_change(change, dryrun):
    project_name = change.get("project")
    number = change.get("number")

    cmd = ["repo", "download", project_name, str(number)]
    cmd_str = " ".join(cmd)

    if not dryrun:
        print("Executing: %s" % (cmd_str,))
        p = subprocess.Popen(cmd)
        p.communicate()
        if p.returncode != 0:
            raise Exception("Cannot execute repo command: %s" % (cmd_str,))
    else:
        print("Would execute: %s" % (cmd_str,))


def nocommand(args, parser):
    parser.print_help(file=sys.stderr)
    return 2


def version(name, args):
    print("repoload (gerrit query tool) version %s" % (__VERSION__,))
    print("License: MIT <https://opensource.org/licenses/MIT>")
    print("Copyright 2019 David Zerulla and Stefan Lengfeld")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Query gerrit and download CR with repo")
    parser.add_argument("--version", dest="version",
                        action="store_true", default=False,
                        help="Show version of program")
    parser.add_argument("--debug", "-d", dest="debug",
                        action="store_true", default=False,
                        help="Enable debug output (e.g. responses from gerrit queries)")

    subparsers = parser.add_subparsers()

    parser_crs = subparsers.add_parser("changes",
                                       help="List all Change Requests.",
                                       aliases=["c"])
    parser_crs.set_defaults(func=print_open_changes)

    parser_topics = subparsers.add_parser("topics",
                                       help="List all topics.",
                                       aliases=["t"])
    parser_topics.set_defaults(func=print_open_topics)

    # TODO Add argument to disable autodetection
    parser_download = subparsers.add_parser("download",
                                       help="Download a single Change (number) request or a whole topic (name).",
                                       aliases=["d"])
    parser_download.set_defaults(func=download)
    parser_download.add_argument("value", help="Change ID or topic name")
    parser_download.add_argument("--dry-run", "-n", dest="dry_run",
                        action="store_true", default=False,
                        help="Just print the repo commands instead of executing.")

    args = parser.parse_args()

    if args.debug:
        global DEBUG
        DEBUG = True

    if args.version:
        ret = version(sys.argv[0], args)
    else:
        # Workaround for help
        if hasattr(args, "func"):
            ret = args.func(args)
        else:
            ret = nocommand(args, parser)
    return ret


if __name__ == '__main__':
    sys.exit(main())
