# coding: UTF-8

import re
import sys
import yaml

class PatternName:
    def __init__(self):
        pass

    DAY = "day"
    PERSON1_STAMP = "person1_stamp"
    PERSON1_TALK = "person1_talk"
    PERSON2_STAMP = "person2_stamp"
    PERSON2_TALK = "person2_talk"
    # TODO: blank を追加


class PatternMatcher:
    def __init__(self, _name1, _name2):
        self.match_map = {}
        self.__pattern_map = {PatternName.DAY: r'20[0-9][0-9]\/[0-1][0-9]\/[0-3][0-9]',
                              PatternName.PERSON1_STAMP: r'[0-2][0-9]:[0-5][0-9]\t{0}\t\[スタンプ\]'.format(_name1),
                              PatternName.PERSON1_TALK: r'[0-2][0-9]:[0-5][0-9]\t{0}'.format(_name1),
                              PatternName.PERSON2_STAMP: r'[0-2][0-9]:[0-5][0-9]\t{0}\t\[スタンプ\]'.format(_name2),
                              PatternName.PERSON2_TALK: r'[0-2][0-9]:[0-5][0-9]\t{0}'.format(_name2)}

        self.__repattern_map = {}
        for patter_name, pattern in self.__pattern_map.items():
            self.__repattern_map[patter_name] = re.compile(pattern)

    def make_match_map(self, _line):
        for patter_name, repattern in self.__repattern_map.items():
            self.match_map[patter_name] = repattern.match(_line)
        return self.match_map


def print_dict(dict):
    for k, v in sorted(dict.items()):
        print k, v


if __name__ == "__main__":
    # 設定ファイルの読み込み
    f = open("conf.yaml")  # 設定ファイルを読み込む
    data = yaml.load(f)
    name1 = data["name"][0]
    name2 = data["name"][1]
    count_words1 = data["count_words1"]
    count_words2 = data["count_words2"]

    # line 履歴テキストの読み込み
    args = sys.argv
    if len(args) < 1:
        print "not a line log file: too short!!"
        sys.exit()
    f = open(args[1])
    line = f.readline()  # 1行を文字列として読み込む(改行文字も含まれる)
    pm = PatternMatcher(name1, name2)

    date = ""
    person1_stamp_num_dict = {}
    person1_talk_num_dict = {}
    person2_stamp_num_dict = {}
    person2_talk_num_dict = {}
    person1_talk_word_len_dict = {}
    person2_talk_word_len_dict = {}
    person1_words1_num = {}
    person2_words1_num = {}
    person1_words2_num = {}
    person2_words2_num = {}
    is_person1 = True

    while line:
        matched_map = pm.make_match_map(line)
        if matched_map[PatternName.DAY]:
            date = matched_map[PatternName.DAY].group(0)
            person1_stamp_num_dict[date] = 0
            person1_talk_num_dict[date] = 0
            person2_stamp_num_dict[date] = 0
            person2_talk_num_dict[date] = 0
            person1_talk_word_len_dict[date] = 0
            person2_talk_word_len_dict[date] = 0
            person1_words1_num[date] = 0
            person2_words1_num[date] = 0
            person1_words2_num[date] = 0
            person2_words2_num[date] = 0
        elif matched_map[PatternName.PERSON1_STAMP]:
            is_person1 = True
            person1_stamp_num_dict[date] += 1
            for word in count_words1:
                person1_words1_num[date] += line.count(word)
            for word in count_words2:
                person1_words2_num[date] += line.count(word)
        elif matched_map[PatternName.PERSON1_TALK]:
            is_person1 = True
            person1_talk_num_dict[date] += 1
            person1_talk_word_len_dict[date] += len(
                line.split('\t')[-1].replace("\n", "").replace("\"", "").decode("utf-8"))
            for word in count_words1:
                person1_words1_num[date] += line.count(word)
            for word in count_words2:
                person1_words2_num[date] += line.count(word)
        elif matched_map[PatternName.PERSON2_STAMP]:
            is_person1 = False
            person2_stamp_num_dict[date] += 1
            for word in count_words1:
                person2_words1_num[date] += line.count(word)
            for word in count_words2:
                person2_words2_num[date] += line.count(word)
        elif matched_map[PatternName.PERSON2_TALK]:
            is_person1 = False
            person2_talk_num_dict[date] += 1
            person2_talk_word_len_dict[date] += len(
                line.split('\t')[-1].replace("\n", "").replace("\"", "").decode("utf-8"))
            for word in count_words1:
                person2_words1_num[date] += line.count(word)
            for word in count_words2:
                person2_words2_num[date] += line.count(word)
        else:
            if is_person1:
                person1_talk_word_len_dict[date] += len(line.replace("\n", "").replace("\"", "").decode("utf-8"))
                for word in count_words1:
                    person1_words1_num[date] += line.count(word)
                for word in count_words2:
                    person1_words2_num[date] += line.count(word)
            else:
                person2_talk_word_len_dict[date] += len(line.replace("\n", "").replace("\"", "").decode("utf-8"))
                for word in count_words1:
                    person2_words1_num[date] += line.count(word)
                for word in count_words2:
                    person2_words2_num[date] += line.count(word)

        line = f.readline()
    f.close

    print "\nperson2_stamp"
    print_dict(person2_stamp_num_dict)

    print "\nperson2_talk"
    print_dict(person2_talk_num_dict)

    print "\nperson2_talk_word_len"
    print_dict(person2_talk_word_len_dict)

    print "\nperson1_stamp"
    print_dict(person1_stamp_num_dict)

    print "\nperson1_talk"
    print_dict(person1_talk_num_dict)

    print "\nperson1_talk_word_len"
    print_dict(person1_talk_word_len_dict)
