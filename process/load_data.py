import datasets

from typing import List, Tuple
import os


def list_cc_files(dir_path: str) -> List[str]:
    return [f for f in os.listdir(dir_path) if f.endswith('.json.gz')]


def _concat_records(tag_records: List[Tuple[str, str]]):
    annotate_text_length = 100
    # タグで分割されているテキストを連結

    concat_records =  ''.join([t[0] for t in tag_records if t[1] in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div']])

    return concat_records
def load_data():
    load_data_dir = "annotated_file/cc"
    list_cc_data_path = [load_data_dir + "/" + p for p in list_cc_files(load_data_dir)][0]

    for gz_path in list_cc_data_path:
        dataset_list = datasets.load_dataset('json',
                                         data_files=list_cc_data_path,
                                         field='tag_records', streaming=True)

        dataset = dataset_list.map(
        lambda x: {'record_id': x['record_id'],
                   'url': x['url'],
                   'title': x['title'],
                   'timestamp': x['timestamp'],
                   'gz_path': gz_path,
                   'text': _concat_records(x['text'])})
    return next(iter(dataset['train']))['text'],next(iter(dataset['train']))['gz_path']

def load_one_gz_data(gz_path:str):

    dataset_list = datasets.load_dataset('json',
                                         data_files=gz_path,
                                         field='tag_records', streaming=True)
    dataset = dataset_list.map(
    lambda x: {'record_id': x['record_id'],
                   'url': x['url'],
                   'title': x['title'],
                   'timestamp': x['timestamp'],
                   'text': _concat_records(x['text'])})
    return next(iter(dataset['train']))['text']

if __name__ == "__main__":
    load_data()
