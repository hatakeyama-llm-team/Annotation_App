import pandas as pd
import streamlit as st
from stqdm import stqdm

from process.load_data import  list_cc_files, load_one_gz_data
from repository.datasets import DataSetsRepository
from repository.evaluate_status import EvaluateStatusRepository


def show():
    st.title("Management")

    if st.button('データセットをDBに登録する'):
        load_data_dir = "annotated_file/cc"
        list_cc_data_path = [load_data_dir + "/" + p for p in list_cc_files(load_data_dir)]
        dataset_repository = DataSetsRepository()

        for gz_path in stqdm(list_cc_data_path):
            try:
                texts = load_one_gz_data(gz_path)

                for i in range(len(texts)//300):
                    data = []
                    data.append((texts[i*300:(i+1)*300],'unprocessed',gz_path))
                    dataset_repository.insertBatch(data)


            except Exception as e:
                st.write(gz_path)
                print(e)
                st.write("error")

    if st.button('アノテーションしたすべてのデータセットを出力する'):
        evaluateStatus = EvaluateStatusRepository()
        df = pd.DataFrame(evaluateStatus.exportAll()).to_csv()
        file = df.encode('utf-8')

        st.download_button("exported.csv", data=file,mime="text/csv")

if __name__ == "__main__":
    if 'user_info' in st.session_state:
        user_name = st.session_state["user_info"]["name"]
        if user_name == 'admin':
            show()
        else:
            st.warning("管理者権限がありません")
    else:
        user_name = ""
        st.warning("管理者権限がありません")


