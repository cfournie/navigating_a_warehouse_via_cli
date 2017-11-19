## Navigating a Data Warehouse via CLI
A talk I gave at Pycon Canada 2017, Montréal, QC, Canada.

`The slides<./slides.htm>` are written in HTML using the `remark<https://github.com/gnab/remark>` framework with graphs created using `mermaid<https://github.com/knsv/mermaid>` and code highlighting using `highlight.js<https://highlightjs.org/>`


### Code
Requires Python 3.6 and either Linux/OSX. To get setup using `pipenv<https://github.com/kennethreitz/pipenv>`, run:

```shell
pipenv --python 3.6
pipenv shell
make install
```

Run tests using:
```shell
make test
make lint
```

Play with scripts using:
```shell
cd scripts
python jobs.py
```
