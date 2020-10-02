# virtool-workflow

An SDK for developing new Virtool workflows.

## Installation

```shell script
git clone https://github.com/virtool/virtool-workflow.git
pip install .

#  Or

pip install git+https://github.com/virtool/virtool-workflow.git
```

This will install both the `virtool_workflow` library and the `workflow` command line utility.

### Usage

Create a **python** file containing an instance of `virtool_workflow.Workflow`.

Execute the workflow using 

```shell script
workflow run -f my_workflow.py
```

Or if the file is named workflow.py

```shell script
workflow run 
```

## Contributing

### Tests

The testing framework used is [pytest](https://docs.pytest.org/en/stable/). Install it using:
```shell script
pip install pytest
```

Run the tests from the root directory:
```shell script
pytest
```

### Documentation

For docstrings, use the [**Sphinx** docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

The packages `sphinx_rtd_theme` and `sphinx_autoapi` are used in rendering the documentation. 

```  shell script
pip install sphinx_rtd_theme sphinx_autoapi
```

#### Markdown for Sphinx

[recommonmark](https://github.com/readthedocs/recommonmark) is used so that Sphinx can 
render documentation from *markdown* files as well as *rst* files. It will need to 
be installed before running `sphinx-build`:

```shell script
pip install recommonmark
```

To use sphinx rst [directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) in a *markdown* file use the 
`eval_rst` [code block](https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext)

#### Building the documentation

```shell script
cd sphinx && make html
```