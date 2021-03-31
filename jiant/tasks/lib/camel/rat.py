from dataclasses import dataclass
from typing import List

from jiant.tasks.core import (
    BaseExample,
    TaskTypes,
)

from jiant.tasks.lib.templates.shared import (
    labels_to_bimap,
)
from jiant.utils.python.datastructures import zip_equal
from jiant.utils.python.io import read_file_lines

from jiant.tasks.lib.udpos import (
    UdposTask,
    DataRow,
    Batch,
    TokenizedExample,
)

ARBITRARY_OVERLY_LONG_WORD_CONSTRAINT = 100
# In a rare number of cases, a single word (usually something like a mis-processed URL)
#  is overly long, and should not be treated as a real multi-subword-token word.
# In these cases, we simply replace it with an UNK token.

@dataclass
class Example(BaseExample):
    guid: str
    tokens: List[str]
    pos_list: List[str]

    def tokenize(self, tokenizer):
        all_tokenized_tokens = []
        labels = []
        label_mask = []
        for token, pos in zip_equal(self.tokens, self.pos_list):
            # Tokenize each "token" separately, assign label only to first token
            tokenized = tokenizer.tokenize(token)
            # If the token can't be tokenized, or is too long, replace with a single <unk>
            if len(tokenized) == 0 or len(tokenized) > ARBITRARY_OVERLY_LONG_WORD_CONSTRAINT:
                tokenized = [tokenizer.unk_token]
            all_tokenized_tokens += tokenized
            padding_length = len(tokenized) - 1
            labels += [CAMeLratTask.LABEL_TO_ID.get(pos, None)] + [None] * padding_length
            label_mask += [1] + [0] * padding_length

        return TokenizedExample(
            guid=self.guid, tokens=all_tokenized_tokens, labels=labels, label_mask=label_mask,
        )


class CAMeLratTask(UdposTask):

    Example = Example
    TokenizedExample = Example
    DataRow = DataRow
    Batch = Batch

    TASK_TYPE = TaskTypes.TAGGING
    LABELS = [
        "n",
        "na",
        "y",
        "i",
        "r",
        "b",
        "u",
    ]

    LABEL_TO_ID, ID_TO_LABEL = labels_to_bimap(LABELS)


    @property
    def num_labels(self):
        return len(self.LABELS)

    def get_train_examples(self):
        return self._create_examples(data_path=self.path_dict["train"], set_type="train")

    def get_val_examples(self):
        return self._create_examples(data_path=self.path_dict["val"], set_type="val")

    def get_test_examples(self):
        return self._create_examples(data_path=self.path_dict["test"], set_type="test")

    @classmethod
    def _create_examples(cls, data_path, set_type):
        curr_token_list, curr_pos_list = [], []
        data_lines = read_file_lines(data_path, "r", encoding="utf-8")
        examples = []
        idx = 0
        for data_line in data_lines:
            data_line = data_line.strip()
            if data_line:
                if set_type == "test":
                    line_tokens = data_line.split("\t")
                    if len(line_tokens) == 2:
                        token, pos = line_tokens
                    else:
                        token, pos = data_line, None
                else:
                    token, pos = data_line.split("\t")
                curr_token_list.append(token)
                curr_pos_list.append(pos)
            else:
                examples.append(
                    Example(
                        guid=f"{set_type}-{idx}", tokens=curr_token_list, pos_list=curr_pos_list,
                    )
                )
                idx += 1
                curr_token_list, curr_pos_list = [], []
        if curr_token_list:
            examples.append(
                Example(guid=f"{set_type}-{idx}", tokens=curr_token_list, pos_list=curr_pos_list)
            )
        return examples