from dataclasses import dataclass
from typing import List

from jiant.tasks.core import (
    BaseExample,
    TaskTypes,
)

from jiant.tasks.lib.templates.shared import (
    labels_to_bimap,
)

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
            labels += [CAMeLposTask.LABEL_TO_ID.get(pos, None)] + [None] * padding_length
            label_mask += [1] + [0] * padding_length

        return TokenizedExample(
            guid=self.guid, tokens=all_tokenized_tokens, labels=labels, label_mask=label_mask,
        )


class CAMeLposTask(UdposTask):

    Example = Example
    TokenizedExample = Example
    DataRow = DataRow
    Batch = Batch

    TASK_TYPE = TaskTypes.TAGGING
    LABELS = [
        "noun",
        "part_neg",
        "pron_rel",
        "noun_num",
        "adv_interrog",
        "part_voc",
        "adj_comp",
        "punc",
        "conj_sub",
        "part_fut",
        "pron_exclam",
        "part",
        "part_verb",
        "verb",
        "digit",
        "conj",
        "pron_interrog",
        "pron",
        "abbrev",
        "part_det",
        "interj",
        "adj_num",
        "adv",
        "part_restrict",
        "adv_rel",
        "adj",
        "prep",
        "part_interrog",
        "verb_pseudo",
        "noun_prop",
        "part_focus",
        "noun_quant",
        "latin",
        "pron_dem",
    ]

    LABEL_TO_ID, ID_TO_LABEL = labels_to_bimap(LABELS)