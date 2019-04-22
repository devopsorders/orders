[![Build Status](https://travis-ci.org/devopsorders/orders.svg?branch=master)](https://travis-ci.org/devopsorders/orders)
[![codecov](https://codecov.io/gh/devopsorders/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/devopsorders/orders)

# Orders Microservice
Orders Microservice for DevOps and Agile Methodologies Stern MBA Class

**Note:** The base service code is contained in `service.py` while the business logic for manipulating Orders is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duities by keeping the model separate from the controller. As such, we have two tests suites: one for the model (`test_orders.py`) and one for the serveice itself (`test_server.py`)

**Note:** This repo uses `python3` as opposed to past repos for this class which used `python2`

**Note:** This repo uses `pytest` as opposed to past repos for this class which used `nosetests`. Nosetests hasn't been updated in years and does not work well with `python3`. See below for instructions on running tests.

## Installation using Vagrant

The easiest way to use this repo is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/devopsorders/orders.git
    cd orders
    vagrant up
    vagrant ssh
    cd /vagrant

You can now run `pytest` to run the tests. As developers we always want to run the tests before we change any code so that we know if we brike the code or perhaps someone before us did? Always run the test cases first!

## Manually running the Tests

Run the tests using `pytest`

    $ pytest

pytest is configured via the included `pytest.ini` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

pytest is also configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

    $ coverage report -m

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases to get higher code coverage.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

    $ flake8 --count --max-complexity=10 --statistics model,service

I've also include `pylint` in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.


BDD tests require the service to be running because unlike the the TDD unit tests that test the code locally, these BDD integration tests are using Selenium to manipulate a web page on a running server.

Run the tests using `behave`

```shell
    $ python run.py &
    $ behave
```

Note that the `&` runs the server in the background. To stop the server, you must bring it to the foreground and then press `Ctrl+C`

Stop the server with

```shell
    $ fg
    $ <ctrl+c>
```

Alternately you can run the server in another `shell` by opening another terminal window and using `vagrant ssh` to establish a second connection to the VM.

When you are done, you can exit and shut down the vm with:

    $ exit
    $ vagrant halt

If the VM is no longer needed you can remove it with:

    $ vagrant destroy


## What's featured in the project?

    * app/service.py -- the main Service using Python Flask
    * app/models.py -- the data model using SQLAlchemy
    * tests/test_server.py -- test cases against the service
    * tests/test_orders.py -- test cases against the Order model

This repo is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created by John Rofrano.
