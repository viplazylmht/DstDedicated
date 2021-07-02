import argparse
import json

def process_notebook(notebook_filename):
    data = {}

    with open(notebook_filename, encoding="utf8") as f:
        data = json.load(f)

    for cell in data['cells']:
        cell['metadata'] = {}
        
        cell['execution_count'] = 'null'
        
        if 'outputId' in cell.keys():
            del cell['outputId']
        if 'id' in cell.keys():
            del cell['id']     

    with open(notebook_filename, 'wt', encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
         
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