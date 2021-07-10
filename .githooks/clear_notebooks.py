# this template was built from this tutorial: https://github.com/mcullan/jupyter-actions

import argparse
import json

def process_notebook(notebook_filename):
    """
    In this action, we clear metadata, set default execution_count, remove id and outputId (gen by google colab) each cell in notebook
    """
    data = {}

    with open(notebook_filename, encoding="utf8") as f:
        data = json.load(f)

    for cell in data['cells']:
        cell['metadata'] = {}
        
        if cell["cell_type"] == 'code':
            cell['execution_count'] = 'null'

            if 'outputs' in cell.keys():

                for o in cell['outputs']:
                    if 'execution_count' in o:
                        o['execution_count'] = 'null'

                    #if 'metadata' in o:
                    #    del o['metadata']

        elif 'execution_count' in cell.keys():
            del cell['execution_count']

        if 'outputId' in cell.keys():
            del cell['outputId']
        if 'id' in cell.keys():
            del cell['id']     

    with open(notebook_filename, 'wt', encoding="utf8") as f:
        transfromed_data = json.dumps(data, ensure_ascii=False, indent=4)

        transfromed_data = transfromed_data.replace('"execution_count": "null"', '"execution_count": null') 

        f.write(transfromed_data)

    print(f"Processed {notebook_filename}")

    return

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='read some notebook files')
    parser.add_argument('notebooks',
                        metavar='Notebooks', 
                        type=str, 
                        nargs='+',
                        help='notebooks')

    args = parser.parse_args()

    notebooks = args.notebooks

    for fn in notebooks:
        if not fn.endswith('.ipynb'):
            print(f'Error: file {fn} is not an IPython notebook.')
            raise
        
    for fn in notebooks:
        process_notebook(fn)