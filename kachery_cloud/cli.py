from email.policy import default
import os
import click
import kachery_cloud as kc


@click.group(help="Kachery cloud command-line client")
def cli():
    pass

@click.command(help="One-time initialization of the kachery cloud client")
def init():
    kc.init()

@click.command(help="Store file in kachery cloud")
@click.argument('filename')
@click.option('--cache-locally', is_flag=True)
@click.option('--label', required=False, default='')
def store_file(filename: str, cache_locally: bool, label: str):
    if label == '': label = os.path.basename(filename)
    uri = kc.store_file(filename, label=label, cache_locally=cache_locally)
    print(uri)

@click.command(help="Store file in kachery cloud")
@click.argument('filename')
@click.option('--label', required=False, default='')
def link_file(filename: str, label: str):
    if label == '': label = os.path.basename(filename)
    uri = kc.link_file(filename, label=label)
    print(uri)

@click.command(help="Load file from kachery cloud")
@click.argument('uri')
@click.option('--dest', required=False, default='')
def load_file(uri: str, dest: str):
    fname = kc.load_file(uri, dest=dest if len(dest) > 0 else None)
    if fname is not None:
        print(fname)

@click.command(help="Load file from kachery cloud")
@click.argument('uri')
def load_file_info(uri: str):
    import json
    x = kc.load_file_info(uri)
    if x is None:
        return
    print(json.dumps(x, indent=4))

@click.command(help="Load file from kachery cloud and write to stdout")
@click.argument('uri')
def cat_file(uri: str):
    kc.cat_file(uri)

@click.command(help="Store file in the local cache")
@click.argument('filename')
@click.option('--reference', is_flag=True)
@click.option('--label', required=False, default='')
def store_file_local(filename: str, reference: bool, label: str):
    if label == '': label = os.path.basename(filename)
    uri = kc.store_file_local(filename, label=label, reference=reference)
    print(uri)

@click.command(help="Share local files")
@click.option('--project', required=False, default='')
def share_local_files_experimental(project: str):
    project = project if project != '' else None
    kc.share_local_files_experimental(project_id=project)

@click.command(help="Request file")
@click.argument('uri')
@click.option('--project', required=True)
def request_file_experimental(uri: str, project: str):
    fname = kc.request_file_experimental(uri, project_id=project)
    print(fname)

cli.add_command(init)
cli.add_command(store_file)
cli.add_command(link_file)
cli.add_command(load_file)
cli.add_command(load_file_info)
cli.add_command(cat_file)
cli.add_command(store_file_local)
cli.add_command(share_local_files_experimental)
cli.add_command(request_file_experimental)