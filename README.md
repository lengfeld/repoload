
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

The installation of `repoload` is possible over PyPI or by directly using the
python script.

PyPI:

    $ python3 -m pip install --user repoload

To manually install the self contained `repoload.py` python script. Just drop
the file in a folder that your environment variable `PATH` references.

Example:

    $ mkdir -p ~/bin
    $ cp repoload/repoload.py ~/bin/repoload
    $ echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
    $ chmod +x ~/bin/repoload  # ensure that the script is executeable

After that the command `repoload` should be available in a newly started shell
and the command

    $ repoload changes

should print a list of open change requests.

Repoload looks for the manifest repository configuration file to determine the
URL of the Gerrit server. It works automatically if the current working
directory is below a `repo` checkout. Alternatively, the environment variable
`ANDROID_BUILD_TOP` can be set to the directory where a `repo` checkout is
located. Finally, the URL can be set directly via the environment variable
`GERRIT_URL`.


## Create and publish a release

To create a release of repoload additional packaging dependency's are needed:

    $ python3 -m pip install --user --upgrade twine setuptools wheel

Next the release which is described in the setup.py file gets packaged.
The version number is taken from the repoload/repoload.py `__VERSION__` string.

    $ python3 setup.py sdist bdist_wheel

As final step the release can be uploaded to PyPI.
See the PyPI documentation on how to configure the credentials for twine.

    $ python3 -m twine upload dist/*


## License

The code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
See the file `COPYING`.


## Contribution

The project is open for contribution. Open a github pull request or send a
patch via email. If you take the patch route, you can find our mail addresses
in the git history easily.

Please add a `Signed-off-by` tag in the commit/patch message to state the
copyright ownership and license information of your patch. Read [Developer
Certificate of Origin v1.1](https://developercertificate.org/) to understand
the meaning and obligations your are taking by adding your sign-off. Thanks in
advance.
