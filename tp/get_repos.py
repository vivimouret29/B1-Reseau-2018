#!/usr/bin/env python3
# coding: utf-8

# Simple script to import all repos from

import argparse

from sys import stdout, stderr, exit
from os import system, mkdir, path

def cloneRepo(repo_url, repo_owner_name, repos_dir):
    """ Clone repo_url repo and place it in tp_number/repos_dir/repo_owner_name
    Returns two arrays which respectively contains :
      - user : url of successfully cloned repos
      - user : url of faulty repos
    """

    # Building the git command
    git_clone_command = ("git clone " + repo_url + " " 
                         + repos_dir + "/" + repo_owner_name
                         + " &> /dev/null")

    stdout.write("\nCloning " + repo_owner_name + "'s repo")

    try:
        # Execute git clone and get return in a var
        command_return = system(git_clone_command)

        # If git command has return 128 : unable to find repo
        # (private repo ? must manually accept invite)
        if command_return == 32768:
            stderr.write("\nCan't clone " + repo_url)
            return False

        stdout.write("\n" + repo_url + " has been cloned.")

        return True

    except Exception as e:
        stderr.write((str(e)))
        stderr.write("\nCan't clone " + repo_url)

        return False


def pullRepo(repo_url, local_repo_path):
    """ Issue a simple 'git pull' from a specific directory
    The directory is repos_dir/repo_owner_name
    """

    try:
        git_pull_command = ("git --git-dir="
                            + local_repo_path
                            + "/.git pull &> /dev/null")

        system(git_pull_command)

        stdout.write("\nRepo " + local_repo_path + " has been pulled")

        return True

    except Exception as e:
        stderr.write((str(e)))
        stderr.write("\nCan't pull in " + local_repo_path
                     + " from " + repo_url)

        return False

# Args handling
parser = argparse.ArgumentParser()

parser.add_argument("tpnumber", type=str,
                    help="Target TP number (mandatory arg)")

# Get script args
args = parser.parse_args()


# GLOBAL VARS

github_urls_file = "./" + args.tpnumber + "/repo_links.csv"
repos_dir = "./" + args.tpnumber + "/repos"

# will be formatted as name:git_connection_string
all_repos = {}

successfully_cloned_repos_owners = []
faulty_repo_owners = []
updated_repo_owners = []

# CODE

# Create destination dir if it does not exist
try:
    mkdir(repos_dir)
except FileExistsError as e:
    pass

# Read github_urls_file and iterate on every lines
# Each line is as follow : "name:github_url"
# We're gonna do the ACTION provided as the script argument on every repo
with open(github_urls_file, "r") as file:

    for line in file.readlines():

        # Standardization of all the strings
        line = line.replace(' ', '')
        line = line.rstrip('/')

        # Gather data from each line
        repo_owner_name = str.capitalize(str.lower(line.split(':')[0]))

        # We're gonna use SSH connection to Github (instead of HTTPS)
        repo_git_url = line.replace('https://', 'git@')
        repo_git_url = repo_git_url.split(':')[1].strip("\n").rstrip('/')
        repo_git_url = repo_git_url.replace('github.com/', 'github.com:')

        local_repo_path = repos_dir + "/" + repo_owner_name

        all_repos[repo_owner_name] = repo_git_url

        # Test if the destination dir exists
        # if yes, pull the repo
        # otherwise, clone it.
        if path.isdir(local_repo_path):
            stdout.write("\nThe repo of " + repo_owner_name
                         + " has already been cloned. Pulling it.")

            if pullRepo(repo_git_url, local_repo_path) is True:
                updated_repo_owners.append(repo_owner_name)

            else:
                faulty_repo_owners.append(repo_owner_name)

        else:
            if cloneRepo(repo_git_url, repo_owner_name, repos_dir) is True:
                successfully_cloned_repos_owners.append(repo_owner_name)

            else:
                faulty_repo_owners.append(repo_owner_name)


# Final print

stdout.write("\nGet " + str(len(all_repos)) + " repos from file :")

stdout.write("\n  " + str(len(faulty_repo_owners)) + " were faulty"
             + "\n  " + str(len(successfully_cloned_repos_owners))
             + " were cloned"
             + "\n  " + str(len(updated_repo_owners)) + " were pulled")

if len(faulty_repo_owners) > 0:
    stdout.write("\n\nFaulty repos (unable to clone) : ")
    for name in faulty_repo_owners:
        stdout.write("\n > " + name + " : " + all_repos[name])

stdout.write("\n")

