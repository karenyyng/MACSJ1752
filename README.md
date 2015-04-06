# Analysis of MACSJ 1752

[Summary](http://www.mergingclustercollaboration.org/macs-j175204440.html) of the system based on existing literature from the Merging Cluster Collaboration.


# Usage 
If you use any part of this repo, please cite Ng et al. (in prep.).

# Contributing - Coding standards 
We adopt the the testing standards from `AstroPy` and use `py.test`. 
And please follow the Python coding style guide [`PEP8`](https://www.python.org/dev/peps/pep-0008/)
If you do not know what `PEP8` is, run your code through
[`autoPEP8`](https://pypi.python.org/pypi/autopep8/1.1) before pushing your
code. 

# Package dependencies 
`pip` is my recommended Python package manager.
I keep track of the packages that I use in
[`package_version.md`](https://github.com/karenyyng/MACSJ1752/blob/master/package_version.md). 
And I make no guarantee that my code works for package versions other than
those listed.
You can install all the package dependencies using:
```
$ pip -r install package_version.md
```
at the command line. But you are really recommended to install a [`virtual
environment`](http://karenyyng.github.io/using-virtualenv-for-safeguarding-research-project-dependencies.html) before you install the packages.
