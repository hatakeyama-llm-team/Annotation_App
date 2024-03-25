import pandas as pd
import streamlit as st

from repository.cloud_sql_mysql.evaluate_status import EvaluateStatusRepository


def show():
    st.title("管理画面")
    # if st.button('データセットをDBに登録する'):
    #     load_data_dir = "annotated_file/takahashi_cc"
    #     list_cc_data_path = [load_data_dir + "/" + p for p in list_cc_files(load_data_dir)]
    #     dataset_repository = DataSetsRepository()
    #     print(list_cc_data_path)
    #     for gz_path in stqdm(list_cc_data_path):
    #         try:
    #             original_texts = load_one_gz_data(gz_path)
    #             cleaned_texts = clean_text(original_texts)
    #             for i in range(len(cleaned_texts)//300):
    #                 data = []
    #                 original_text = cleaned_texts[i*300:(i+1)*300]
    #                 cleaned_text = clean_text(original_text)
    #                 if cleaned_text:
    #                     data.append((cleaned_text,original_text,'unprocessed',gz_path))
    #                     dataset_repository.insertBatch(data)
    #                 else:
    #                     pass
    #
    #         except Exception as e:
    #             st.write(gz_path)
    #             print(e)
    #             st.write("error")

    # if st.button('jsonlのデータをDBに登録する'):
    #     list_cc_data_path = [
    #         'annotated_file/cleaned_cc_hatakeyama/random_sample.jsonl',
    #     ]
    #     dataset_repository = DataSetsRepository()
    #     for jsonl_path in stqdm(list_cc_data_path):
    #         try:
    #             original_cleaned_texts = load_one_jsonl_data(jsonl_path)
    #             for cleaned_text in original_cleaned_texts:
    #                 data = []
    #                 if cleaned_text:
    #                     data.append((cleaned_text,'','unprocessed',jsonl_path))
    #                     dataset_repository.insertBatch(data)
    #                 else:
    #                     pass
    #
    #         except Exception as e:
    #             st.write(jsonl_path)
    #             print(e)
    #             st.write("error")

    def export_dataset():
        evaluateStatus = EvaluateStatusRepository()
        df = pd.DataFrame(evaluateStatus.exportAll(),
                          columns=['dataset_id', 'evaluated_point', 'annotated_text', 'feedback_text','text_category']).to_csv()
        file = df.encode('utf-8')
        return file

    if st.button('アノテーションしたすべてのデータセットを出力する'):
        st.download_button("annotation.csv", data=export_dataset(),mime="text/csv")

if __name__ == "__main__":
    show()


