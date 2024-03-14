import streamlit as st
from stqdm import stqdm

from process.auth import check_login
from process.load_data import load_data, list_cc_files, load_one_gz_data
from process.segment import segment
from repository.datasets import DataSetsRepository


def main():
    st.title("Management")

    st.write("データを書き出す")
    if st.button('Save Progress'):
        load_data_dir = "annotated_file/cc"
        list_cc_data_path = [load_data_dir + "/" + p for p in list_cc_files(load_data_dir)]
        for gz_path in list_cc_data_path:
            try:
                texts = load_one_gz_data(gz_path)
                texts_segmented = segment(texts)
                for text in stqdm(texts_segmented):
                    data = []
                    data.append((text,'unprocessed',gz_path))
                    dataset_repository = DataSetsRepository()
                    dataset_repository.insertBatch(data)
            except Exception as e:
                st.write(gz_path)
                st.write("error")

if __name__ == "__main__":
    # check_login()

    main()