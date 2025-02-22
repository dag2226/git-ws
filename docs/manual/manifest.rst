.. _manifest_manual:

Manifest
========

The main purpose of Git Workspace is to be able to compose a workspace consisting of one or more ``git`` repositories. For this, a single repository can define meta information including a list of dependencies to other ``git`` repositories. These information are stored in a file called ``git-ws.toml``. To generate that file, all you need to do is running the following command inside your project:

.. code-block:: bash

    git ws manifest create

This will create a template for the manifest file that you can edit to fit your needs. The standard file created is self-documenting, so it should be relatively easy to get started with it:


.. include:: ../static/git-ws.toml
    :code: toml

In the following, the various parts of a manifest file are described.


.. _manifest_defaults:

The ``defaults`` section
------------------------


.. _manifest_dependencies:

The ``dependencies`` section
----------------------------


.. _manifest_remotes:

The ``remotes`` section
-----------------------


.. _manifest_group_filters:

The ``group-filters`` section
-----------------------------


.. _manifest_copyfiles:

The ``copyfiles`` section
-----------------------------


.. _manifest_linkfilkes:

The ``linkfiles`` section
-----------------------------
