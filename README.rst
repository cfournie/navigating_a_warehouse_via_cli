Navigating a Data Warehouse via CLI
=============

A talk I gave at Pycon Canada 2017, Montréal, QC, Canada.

`These slides <./slides/index.htm>`_ [`PDF <slides/slides.pdf>`_] are written in HTML using the `remark <https://github.com/gnab/remark>`_ framework with graphs created using `mermaid <https://github.com/knsv/mermaid>`_ and code highlighting using `highlight.js <https://highlightjs.org/>`_.


Code
----
Requires Python 3.6 and either Linux/OSX. To get setup using `pipenv <https://github.com/kennethreitz/pipenv>`_, run::

    pipenv --python 3.6
    pipenv shell
    make install


Run tests using::

    make test
    make lint


Play with scripts using::

    cd scripts
    python jobs.py

