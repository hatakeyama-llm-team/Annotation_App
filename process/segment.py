import functools
# from locale import normalize

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.split.simple_splitter import split_punctuation, split_newline


# Todo:データはできるだけ消さない、加工しないようにする。
def segment(data):
    '''日本語の文章を分割する'''
    split_punc2 = functools.partial(split_punctuation, punctuations=r".。 !?")
    concat_tail_no = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(の)$",
                                       remove_former_matched=False)
    concat_decimal = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(\d.)$",
                                       latter_matching_rule=r"^(\d)(?P<result>.+)$", remove_former_matched=False,
                                       remove_latter_matched=False)
    segmenter = make_pipeline( split_newline, concat_tail_no, split_punc2, concat_decimal)
    # 文字を区切るだけにする
    # 正規化はしない。
    # segmenter = make_pipeline(normalize, split_newline, concat_tail_no, split_punc2, concat_decimal)
    return list(segmenter(data))

