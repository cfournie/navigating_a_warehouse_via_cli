
.. image:: https://travis-ci.org/cfournie/navigating_a_warehouse_via_cli.svg?branch=master
    :target: https://travis-ci.org/cfournie/navigating_a_warehouse_via_cli

Navigating a Data Warehouse via CLI
=============

This repository contains a talk (and its accompanying code) that I gave at Pycon Canada 2017, Montréal, QC, Canada.

The `slides <./slides/index.htm>`_ [`PDF <slides/slides.pdf>`_] are written in HTML using the `remark <https://github.com/gnab/remark>`_ js framework with graphs created using `mermaid <https://github.com/knsv/mermaid>`_ js and code highlighting using `highlight.js <https://highlightjs.org/>`_.


Code 
----
Requires Python 3.6 and either Linux/OSX.

Clone this repository and go into the directory::

    git clone https://github.com/cfournie/navigating_a_warehouse_via_cli.git
    cd navigating_a_warehouse_via_cli

Start your virtualenv (e.g. using `pipenv <https://github.com/kennethreitz/pipenv>`_ by running ``pipenv --python 3.6`` followed by ``pipenv shell``) and then install dependencies using::
    
    make install


Run tests using::

    make test
    make lint


Play with scripts using::

    cd scripts
    python jobs.py

