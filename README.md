NoDesk Server
======
NoDesk Server is the back-end of the NoDesk App.
It is written in Python and uses Django.


Setup
=====

Setup virtualenv
------------------

With virtualenv, you will create a virtual Python environment in which
you can install dependencies for nodesk without altering your system
(i.e., without requiring root), while isolating the dependencies:
you'll be sure to have the right version of any requirement.

Install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/):
  apt-get install virtualenvwrapper

Create the virtualenv:
  mkvirtualenv nodesk

You can exit the virtualenv with:
  deactivate

To enter the virtualenv again:
  workon nodesk


Run nodesk
------------

  cd nodesk_server
  ./manage.py runserver







