
.. image:: https://travis-ci.org/cfournie/navigating_a_warehouse_via_cli.svg?branch=master
    :target: https://travis-ci.org/cfournie/navigating_a_warehouse_via_cli

Navigating a Data Warehouse via CLI
=============

This repository contains a talk (and its accompanying code) that I gave at Pycon Canada 2017, Montréal, QC, Canada.

**Abstract**: At Shopify we have over 3000 Python batch ETL jobs in our data warehouse arranged in a directed graph producing data between them. Navigating this graph to assess the impact of bugs is challenging. To solve this, we’ve made Python CLI tools that combined with other Unix tools help us reason about these jobs.

Slides
----
The `slides <./slides/index.htm>`_ [`PDF <slides/slides.pdf>`_] are written in HTML using the `remark <https://github.com/gnab/remark>`_ js framework with graphs created using `mermaid <https://github.com/knsv/mermaid>`_ js and code highlighting using `highlight.js <https://highlightjs.org/>`_.

You might ask, "why are some of the slides blank?" That's because I gave a live-demo of some scripts (provided in this repo) during those slides. You can see what I ran by reading the speakers notes in the HTML version of the slides. When the video of the talk is posted I'll add a link to it here.


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

