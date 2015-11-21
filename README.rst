===============
 nose-mp-split
===============

This plugin adds ``_multiprocess_can_split_ = True`` to each of your test
classes and modules. That's all. This tells nose's multiprocess plugin that it
doesn't need to run all of a class's tests in the same process. Nose will then
distribute test cases from the same class (or module) across different
processes. It was written in response to behavior demonstrated here_.

When it's safe to use with your tests, this plugin is so cool!

- There's no need to edit your tests to contain a nose-specific flag.
- It evenly distributes test cases (rather than test classes) across processes.
  This utilizes worker process better to speed up test runs, especially if one
  class has many tests cases and takes much longer to run than the others.
- It produces more responsive output. Since nose runs test *classes* in worker
  processes, it waits until each class has finished before printing the results
  for that class. This plugin ensures the results of a test case are printed
  immediately after that test has finished.

You can use this plugin when you know your tests are safe to run in parallel.
For instance, don't use this plugin if you have test fixtures that cannot
be run repeatedly and concurrently in multiple processes.

Quickstart
==========

.. code-block:: shell

    $ pip install nose-mp-split
    $ nosetests --mp-split-all --processes=4 mytests/

``nose-mp-split`` has no effect when not running tests in multiple processes.

.. _here: https://github.com/pglass/nosemultiprocess-test
