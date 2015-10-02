import os
import json
import click
import pypi2nix.py2txt
import pypi2nix.cfg2txt
import pypi2nix.txt2json
import pypi2nix.json2wheels


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def main(input_file):

    i = lambda end: input_file.endswith(end) and input_file or None

    py_file = i('setup.py')
    cfg_file = i('.cfg')
    txt_file = i('.txt')
    json_file = i('.json')
    wheels_file = i('.wheels')
    nix_file = None

    # TODO: more asserts and raise ClickExceptions
    #if any(py_file, cfg_file, txt_file, json_file, wheels_file):
    #    raise Exception(
    #        '<input_file> was not correct type. check help for more info.')

    #
    # Stage 1
    #
    # from setup.py or buildout.cfg we create complete list of all requirements
    # needed.
    #
    if py_file:
        click.secho('Converting setup.py to requirements.txt', fg='yellow')
        txt_file = pypi2nix.py2txt.do(py_file)
        click.secho('Got %s' % txt_file, fg='green')

    elif cfg_file:
        click.secho('Converting %s to requirements.txt' % cfg_file, fg='yellow')
        txt_file = pypi2nix.cfg2txt.do(cfg_file)
        click.secho('Got %s' % txt_file, fg='green')

    #
    # Stage 2
    #
    # once we have all the metadata we can create wheels and install them, so
    # that metadata.json is produced for each package which we process to
    # extract dependencies for packages

    # returns a list of dicts, eg:
    # [
    #   dict(name=..., url=..., md5=..., deps=[...<list-of names>...]),
    #   ...
    # ]
    if json_file:
        if type(json_file) != list:
            with open(json_file) as f:
                json_file = json.load(f)

        click.secho('Converting %s to wheels' % json_file, fg='yellow')
        wheels_file = pypi2nix.json2wheels.do(json_file)
        click.secho('Got %s' % wheels_file, fg='green')

    #
    # Stage 3
    #
    # With all above we can now generate nix expressions
    #
    if wheels_file:
        click.secho('Converting %s to nix' % wheels_file, fg='yellow')
        nix_file = pypi2nix.wheels2nix.do(wheels_file)
        click.secho('Got %s' % nix_file, fg='green')

if __name__ == "__main__":
    main()