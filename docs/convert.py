"""
Convert Jupyter notebook to html
"""
import os
import json
from nbconvert import HTMLExporter

INDEX_HTML_PATH = os.path.join('docs', 'index.html')
TEMPLATE_PATH = os.path.join('docs', 'templates')


def gen_notebook_path():
    if not os.path.exists(INDEX_HTML_PATH):
        last_render_datetime = 0
    else:
        last_render_datetime = os.path.getmtime(INDEX_HTML_PATH)
    flt = lambda f: f.endswith('.ipynb') and 'checkpoint' not in f
    for dirpath, dirnames, filenames in os.walk(os.path.join('docs', 'source_notebooks')):
        for filename in filter(flt, filenames):
            source_ipynb_path = os.path.join(dirpath, filename)
            modified_datetime = os.path.getmtime(source_ipynb_path)
            if modified_datetime > last_render_datetime:
                yield source_ipynb_path


def arrange_notebook_execution_order(source_ipynb_path):
    with open(source_ipynb_path, 'rt', encoding='utf-8') as f:
        notebook = json.load(f)
    cnt = 1
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            cell['execution_count'] = cnt
            if cell['outputs']:
                assert len(cell['outputs']) == 1
                cell['outputs'][0]['execution_count'] = cnt
            cnt += 1

    with open(source_ipynb_path, 'wt', encoding='utf-8') as f:
        json.dump(notebook, f)


def convert():
    exporter = HTMLExporter()
    exporter.template_path = [os.path.join('docs', 'templates')]
    exporter.template_file = 'full'
    for source_ipynb_path in gen_notebook_path():
        arrange_notebook_execution_order(source_ipynb_path)
        _, filename = os.path.split(source_ipynb_path)

        body, _ = exporter.from_filename(source_ipynb_path)
        write_path = os.path.join('docs', filename.replace('ipynb', 'html'))
        with open(write_path, 'wt', encoding='utf-8') as f:
            f.write(body)
        print('{} write success.'.format(write_path))


def main():
    convert()


if __name__ == '__main__':
    main()
