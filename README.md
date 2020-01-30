
# Repoload - a change request download tool

`repoload` is a commandline tool, written in python3, that should make your
life and daily work with the [repo tool][repo] and the [gerrit review
system][gerrit] more pleasant.

`repoload` has currently only a very limited set of functionalities and a lot
of `TODOS` in the code, but it's already useful. The possibility to download
multiple CRs (Change Requests) by naming the crossrepo topic is the *must-have*
feature, because it's not supported by `repo` itself.

The full feature list is:

* Query gerrit for open CRs
* Query gerrit for open topic names
* Download a CR or multiple CRs linked by a topic at once.

It also works with gerrit using the [autosubmitter plugin][autosubmit].

[repo]: https://gerrit.googlesource.com/git-repo/
[gerrit]: https://www.gerritcodereview.com/
[autosubmit]: https://gerrit.googlesource.com/plugins/autosubmitter


## Usage

Before using `repoload` you have to install the script and configure the gerrit
server URL. See below.

The primary use case of `repoload` is to easily checkout `crossrepo/` CRs
(Change Requests) from gerrit.

Example:

     # Change directory into the repo checkout
     $ cd to/repo/checkout

     # Bring your repo checkout into a consistent state
     # Beware: 'repo sync' maybe drops your local modifications without a warning
     # Backup your code changes!
     $ repo sync

     # Query the gerrit server for open CRs
     # You can use `grep` to filter for your coworker's CRs
     $ repoload changes | grep -i john
     123: Add feature A (Jon Doe <john.doe@my.corp.com>) [topic: crossrepo/feature-a]
     128: Update library for feature A (John Doe <john.doe@my.corp.com>) [topic: crossrepo/feature-a]
     [...]

     # For downloading all CRs linked by a topic, just use the topic name
     $ repload download crossrepo/feature-a

     # For downloading only a single CR, use the CR number
     $ repload download 123

     # Build, test and have fun.

All `repoload` commands have an abbreviation:

     $ repoload c     # for 'changes'
     $ repoload t     # for 'topics'
     $ repoload d     # for 'download'


For further information see:

     $ repoload --help
     $ repoload download --help    # and so forth


## Installation

The python script `repoload.py` is self contained.  Just drop the file
in a folder that your environment variable `PATH` references.

Example:

    $ mkdir -p ~/bin
    $ cp repoload.py ~/bin/repoload
    $ echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
    $ chmod +x ~/bin/repoload  # ensure that the script is executeable

After that the command `repoload` should be available in a newly started shell.

Now you have to configure the gerrit URL of your workplace's gerrit server. It
must support ssh access. The script uses the environment variable `GERRIT_URL`.

Example:

    $ echo 'export GERRIT_URL=gerrit.my.corp.com' >> ~/.bashrc

After that the command

    $ repoload changes

should print a list of open change requests.


## License

The code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
See the file `COPYING`.
