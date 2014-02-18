Project Liquid
==============

Project Liquid is the codename of the new ACM@UIUC website.

The master branch should always be an up to date working version of the website. Please do all
developement in a Github fork and submit a Pull Request when the feature is ready to launch. It
is good form and easier if you keep each feature in a seperate branch on your fork.

Issues and Feature Requests
---------------------------
Please use the github issue tracker to track tasks and current work.

Getting Started
---------------
To get started, fork the repository on Github so you have your own little plot of the internet
to work with. Next, checkout that repo!

    git clone git@github.com:USERNAME/liquid.git

After cloning to your computer you need to have the following system packages installed:
* mysql
  * MAC: `brew install mysql` then `mysql.server start`
  * Linux: `sudo apt-get install mysql-server`

An important step in any Python project is setting up a sanitary work environment. You don't
cook in a messy kitchen, do you?

    cd liquid
    virtualenv venv
    source venv/bin/activate # run this whenever you open a new terminal session

Now we need to grab all of the Python packages:

    pip install -r liquid/requirements.txt

Note there is a problem with certain versions of Pip and speciic packages. It works fine on Pip 1.0ish.

Run the fancy-shmancy script that will setup the database into an initial state.

    python setup.py

Now let's start the website!

    python liquid/manage.py runserver

Visit [localhost:8000](http://localhost:8000) in your browser.

Note that you will not be able to login unless you are on the UIUC campus network. If you want
to work remotely, check out [CITES VPN](https://www.cites.illinois.edu/vpn/download-install.html).

How to Submit a Pull Request
----------------------------
So you've gone through the setup above, eh? Ready to get to work? Good!

Add the acm-uiuc/liquid repository as a remote so you can pull in new changes from everyone else.

    git remote add acm https://github.com/acm-uiuc/liquid.git
    git fetch

Do the following whenever you want to pull in changes from the main repository.

    git checkout master
    git pull acm master

Now you will want to make each independant feature or bug-fix on a different branch. This keeps
things tidy and lets everyone code review pull requests in small chunks. Let's make a new branch,
do some work, and commit.

    git checkout -b feature
    # make changes ...
    git commit -m "Feature X: description."

In order to make a pull request, you need to push your changes back up to Github.

    git push -u origin feature

Now if you go to the [acm-uiuc/liquid](https://github.com/acm-uiuc/liquid) repository and make a pull
request. After creating it, sit back and wait for the sweet, sweet praise to come in.

Sometimes (most of the time), the code reviewers will say "Hey you! You're wrong! Fix this! Change that!".
Relax, we got this. Checkout your feature branch again, make your changes, and push it back up to Github.

    git checkout feature
    # make changes ...
    git commit -m "I fixed it, yo."
    git push

Your pull request will be automagically updated.

*Note*: It's important that you don't push commits that are not related to this pull request up to this
branch. They will be added to the pull request and everything will get very mixed up. To check what branch
you are on, use `git branch` or `git status`.

Troubleshooting
---------------

* Python-LDAP won't install
  * Mac: OS X formerly had problems that were solved by instructions [here](http://projects.skurfer.com/posts/2011/python_ldap_lion/).
  * Linux: Try `sudo apt-get install python-ldap`
