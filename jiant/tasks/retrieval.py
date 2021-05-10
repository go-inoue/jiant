import os
from typing import Optional

from jiant.tasks.lib.abductive_nli import AbductiveNliTask
from jiant.tasks.lib.acceptability_judgement.definiteness import AcceptabilityDefinitenessTask
from jiant.tasks.lib.acceptability_judgement.coord import AcceptabilityCoordTask
from jiant.tasks.lib.acceptability_judgement.eos import AcceptabilityEOSTask
from jiant.tasks.lib.acceptability_judgement.whwords import AcceptabilityWHwordsTask
from jiant.tasks.lib.adversarial_nli import AdversarialNliTask
from jiant.tasks.lib.arc_easy import ArcEasyTask
from jiant.tasks.lib.arc_challenge import ArcChallengeTask
from jiant.tasks.lib.boolq import BoolQTask
from jiant.tasks.lib.bucc2018 import Bucc2018Task
from jiant.tasks.lib.ccg import CCGTask
from jiant.tasks.lib.cola import ColaTask
from jiant.tasks.lib.commitmentbank import CommitmentBankTask
from jiant.tasks.lib.commonsenseqa import CommonsenseQATask
from jiant.tasks.lib.edge_probing.nonterminal import NonterminalTask
from jiant.tasks.lib.copa import CopaTask
from jiant.tasks.lib.edge_probing.coref import CorefTask
from jiant.tasks.lib.cosmosqa import CosmosQATask
from jiant.tasks.lib.edge_probing.dep import DepTask
from jiant.tasks.lib.edge_probing.dpr import DprTask
from jiant.tasks.lib.fever_nli import FeverNliTask
from jiant.tasks.lib.glue_diagnostics import GlueDiagnosticsTask
from jiant.tasks.lib.hellaswag import HellaSwagTask
from jiant.tasks.lib.mctaco import MCTACOTask
from jiant.tasks.lib.mctest import MCTestTask
from jiant.tasks.lib.mlm_simple import MLMSimpleTask
from jiant.tasks.lib.mlm_premasked import MLMPremaskedTask
from jiant.tasks.lib.mlm_pretokenized import MLMPretokenizedTask
from jiant.tasks.lib.mlqa import MlqaTask
from jiant.tasks.lib.mnli import MnliTask
from jiant.tasks.lib.mnli_mismatched import MnliMismatchedTask
from jiant.tasks.lib.mrpc import MrpcTask
from jiant.tasks.lib.mrqa_natural_questions import MrqaNaturalQuestionsTask
from jiant.tasks.lib.multirc import MultiRCTask
from jiant.tasks.lib.mutual import MutualTask
from jiant.tasks.lib.mutual_plus import MutualPlusTask
from jiant.tasks.lib.edge_probing.ner import NerTask
from jiant.tasks.lib.newsqa import NewsQATask
from jiant.tasks.lib.panx import PanxTask
from jiant.tasks.lib.pawsx import PawsXTask
from jiant.tasks.lib.edge_probing.pos import PosTask
from jiant.tasks.lib.qamr import QAMRTask
from jiant.tasks.lib.qasrl import QASRLTask
from jiant.tasks.lib.qqp import QqpTask
from jiant.tasks.lib.qnli import QnliTask
from jiant.tasks.lib.quail import QuailTask
from jiant.tasks.lib.quoref import QuorefTask
from jiant.tasks.lib.race import RaceTask
from jiant.tasks.lib.record import ReCoRDTask
from jiant.tasks.lib.rte import RteTask
from jiant.tasks.lib.ropes import RopesTask
from jiant.tasks.lib.scitail import SciTailTask
from jiant.tasks.lib.edge_probing.semeval import SemevalTask
from jiant.tasks.lib.snli import SnliTask
from jiant.tasks.lib.socialiqa import SocialIQATask
from jiant.tasks.lib.edge_probing.spr1 import Spr1Task
from jiant.tasks.lib.edge_probing.spr2 import Spr2Task
from jiant.tasks.lib.squad import SquadTask
from jiant.tasks.lib.edge_probing.srl import SrlTask
from jiant.tasks.lib.senteval.bigram_shift import SentEvalBigramShiftTask
from jiant.tasks.lib.senteval.coordination_inversion import SentEvalCoordinationInversionTask
from jiant.tasks.lib.senteval.obj_number import SentEvalObjNumberTask
from jiant.tasks.lib.senteval.odd_man_out import SentEvalOddManOutTask
from jiant.tasks.lib.senteval.past_present import SentEvalPastPresentTask
from jiant.tasks.lib.senteval.sentence_length import SentEvalSentenceLengthTask
from jiant.tasks.lib.senteval.subj_number import SentEvalSubjNumberTask
from jiant.tasks.lib.senteval.top_constituents import SentEvalTopConstituentsTask
from jiant.tasks.lib.senteval.tree_depth import SentEvalTreeDepthTask
from jiant.tasks.lib.senteval.word_content import SentEvalWordContentTask
from jiant.tasks.lib.sst import SstTask
from jiant.tasks.lib.stsb import StsbTask
from jiant.tasks.lib.superglue_axg import SuperglueWinogenderDiagnosticsTask
from jiant.tasks.lib.superglue_axb import SuperglueBroadcoverageDiagnosticsTask
from jiant.tasks.lib.swag import SWAGTask
from jiant.tasks.lib.tatoeba import TatoebaTask
from jiant.tasks.lib.tydiqa import TyDiQATask
from jiant.tasks.lib.udpos import UdposTask
from jiant.tasks.lib.wic import WiCTask
from jiant.tasks.lib.wnli import WnliTask
from jiant.tasks.lib.wsc import WSCTask
from jiant.tasks.lib.xnli import XnliTask
from jiant.tasks.lib.xquad import XquadTask
from jiant.tasks.lib.mcscript import MCScriptTask
from jiant.tasks.lib.arct import ArctTask
from jiant.tasks.lib.winogrande import WinograndeTask
from jiant.tasks.lib.piqa import PiqaTask
# CAMeL
from jiant.tasks.lib.camel.pos import CAMeLposTask
from jiant.tasks.lib.camel.prc3 import CAMeLprc3Task
from jiant.tasks.lib.camel.prc2 import CAMeLprc2Task
from jiant.tasks.lib.camel.prc1 import CAMeLprc1Task
from jiant.tasks.lib.camel.prc0 import CAMeLprc0Task
from jiant.tasks.lib.camel.per import CAMeLperTask
from jiant.tasks.lib.camel.asp import CAMeLaspTask
from jiant.tasks.lib.camel.vox import CAMeLvoxTask
from jiant.tasks.lib.camel.mod import CAMeLmodTask
from jiant.tasks.lib.camel.form_gen import CAMeLform_genTask
from jiant.tasks.lib.camel.gen import CAMeLgenTask
from jiant.tasks.lib.camel.form_num import CAMeLform_numTask
from jiant.tasks.lib.camel.num import CAMeLnumTask
from jiant.tasks.lib.camel.stt import CAMeLsttTask
from jiant.tasks.lib.camel.cas import CAMeLcasTask
from jiant.tasks.lib.camel.enc0 import CAMeLenc0Task
from jiant.tasks.lib.camel.rat import CAMeLratTask
# CAMeL combination
from jiant.tasks.lib.camel_cmb.per__gen__num import CAMeLper__gen__numTask
from jiant.tasks.lib.camel_cmb.per__form_gen__form_num import CAMeLper__form_gen__form_numTask
from jiant.tasks.lib.camel_cmb.asp__mod__vox import CAMeLasp__mod__voxTask
from jiant.tasks.lib.camel_cmb.cas__stt import CAMeLcas__sttTask
from jiant.tasks.lib.camel_cmb.prc3__prc2__prc1__prc0__enc0 import CAMeLprc3__prc2__prc1__prc0__enc0Task
from jiant.tasks.lib.camel_cmb.gen__num__rat import CAMeLgen__num__ratTask
from jiant.tasks.lib.camel_cmb.pos__per__gen__num import CAMeLpos__per__gen__numTask
from jiant.tasks.lib.camel_cmb.pos__per__form_gen__form_num import CAMeLpos__per__form_gen__form_numTask
from jiant.tasks.lib.camel_cmb.pos__asp__mod__vox import CAMeLpos__asp__mod__voxTask
from jiant.tasks.lib.camel_cmb.pos__cas__stt import CAMeLpos__cas__sttTask
from jiant.tasks.lib.camel_cmb.pos__prc3__prc2__prc1__prc0__enc0 import CAMeLpos__prc3__prc2__prc1__prc0__enc0Task
from jiant.tasks.lib.camel_cmb.pos__gen__num__rat import CAMeLpos__gen__num__ratTask
from jiant.tasks.lib.camel_cmb.per__gen__num__rat import CAMeLper__gen__num__ratTask
from jiant.tasks.lib.camel_cmb.pos__per__gen__num__rat import CAMeLpos__per__gen__num__ratTask
from jiant.tasks.lib.camel_cmb.tags17 import CAMeLtags17Task
from jiant.tasks.lib.camel_cmb.tags14 import CAMeLtags14Task
# CAMeLGLF
from jiant.tasks.lib.camel_glf.pos import CAMeLGLFposTask
from jiant.tasks.lib.camel_glf.prc3 import CAMeLGLFprc3Task
from jiant.tasks.lib.camel_glf.prc2 import CAMeLGLFprc2Task
from jiant.tasks.lib.camel_glf.prc1 import CAMeLGLFprc1Task
from jiant.tasks.lib.camel_glf.prc0 import CAMeLGLFprc0Task
from jiant.tasks.lib.camel_glf.per import CAMeLGLFperTask
from jiant.tasks.lib.camel_glf.asp import CAMeLGLFaspTask
from jiant.tasks.lib.camel_glf.vox import CAMeLGLFvoxTask
from jiant.tasks.lib.camel_glf.mod import CAMeLGLFmodTask
from jiant.tasks.lib.camel_glf.form_gen import CAMeLGLFform_genTask
from jiant.tasks.lib.camel_glf.form_num import CAMeLGLFform_numTask
from jiant.tasks.lib.camel_glf.stt import CAMeLGLFsttTask
from jiant.tasks.lib.camel_glf.cas import CAMeLGLFcasTask
from jiant.tasks.lib.camel_glf.enc0 import CAMeLGLFenc0Task
from jiant.tasks.lib.camel_glf.enc1 import CAMeLGLFenc1Task
from jiant.tasks.lib.camel_glf.enc2 import CAMeLGLFenc2Task
# CAMeLEGY
from jiant.tasks.lib.camel_egy.pos import CAMeLEGYposTask
from jiant.tasks.lib.camel_egy.prc3 import CAMeLEGYprc3Task
from jiant.tasks.lib.camel_egy.prc2 import CAMeLEGYprc2Task
from jiant.tasks.lib.camel_egy.prc1 import CAMeLEGYprc1Task
from jiant.tasks.lib.camel_egy.prc0 import CAMeLEGYprc0Task
from jiant.tasks.lib.camel_egy.per import CAMeLEGYperTask
from jiant.tasks.lib.camel_egy.asp import CAMeLEGYaspTask
from jiant.tasks.lib.camel_egy.vox import CAMeLEGYvoxTask
from jiant.tasks.lib.camel_egy.mod import CAMeLEGYmodTask
from jiant.tasks.lib.camel_egy.form_gen import CAMeLEGYform_genTask
from jiant.tasks.lib.camel_egy.form_num import CAMeLEGYform_numTask
from jiant.tasks.lib.camel_egy.stt import CAMeLEGYsttTask
from jiant.tasks.lib.camel_egy.cas import CAMeLEGYcasTask
from jiant.tasks.lib.camel_egy.enc0 import CAMeLEGYenc0Task
from jiant.tasks.lib.camel_egy.enc1 import CAMeLEGYenc1Task
from jiant.tasks.lib.camel_egy.enc2 import CAMeLEGYenc2Task
# CAMeLLEV
from jiant.tasks.lib.camel_lev.pos import CAMeLLEVposTask
from jiant.tasks.lib.camel_lev.prc3 import CAMeLLEVprc3Task
from jiant.tasks.lib.camel_lev.prc2 import CAMeLLEVprc2Task
from jiant.tasks.lib.camel_lev.prc1 import CAMeLLEVprc1Task
from jiant.tasks.lib.camel_lev.prc0 import CAMeLLEVprc0Task
from jiant.tasks.lib.camel_lev.per import CAMeLLEVperTask
from jiant.tasks.lib.camel_lev.asp import CAMeLLEVaspTask
from jiant.tasks.lib.camel_lev.vox import CAMeLLEVvoxTask
from jiant.tasks.lib.camel_lev.mod import CAMeLLEVmodTask
from jiant.tasks.lib.camel_lev.form_gen import CAMeLLEVform_genTask
from jiant.tasks.lib.camel_lev.form_num import CAMeLLEVform_numTask
from jiant.tasks.lib.camel_lev.stt import CAMeLLEVsttTask
from jiant.tasks.lib.camel_lev.cas import CAMeLLEVcasTask
from jiant.tasks.lib.camel_lev.enc0 import CAMeLLEVenc0Task
from jiant.tasks.lib.camel_lev.enc1 import CAMeLLEVenc1Task
from jiant.tasks.lib.camel_lev.enc2 import CAMeLLEVenc2Task


from jiant.tasks.core import Task
from jiant.utils.python.io import read_json


TASK_DICT = {
    "abductive_nli": AbductiveNliTask,
    "arc_easy": ArcEasyTask,
    "arc_challenge": ArcChallengeTask,
    "superglue_axg": SuperglueWinogenderDiagnosticsTask,
    "acceptability_definiteness": AcceptabilityDefinitenessTask,
    "acceptability_coord": AcceptabilityCoordTask,
    "acceptability_eos": AcceptabilityEOSTask,
    "acceptability_whwords": AcceptabilityWHwordsTask,
    "adversarial_nli": AdversarialNliTask,
    "boolq": BoolQTask,
    "bucc2018": Bucc2018Task,
    "cb": CommitmentBankTask,
    "ccg": CCGTask,
    "cola": ColaTask,
    "commonsenseqa": CommonsenseQATask,
    "nonterminal": NonterminalTask,
    "copa": CopaTask,
    "coref": CorefTask,
    "cosmosqa": CosmosQATask,
    "dep": DepTask,
    "dpr": DprTask,
    "fever_nli": FeverNliTask,
    "glue_diagnostics": GlueDiagnosticsTask,
    "hellaswag": HellaSwagTask,
    "mctaco": MCTACOTask,
    "mctest": MCTestTask,
    "mlm_simple": MLMSimpleTask,
    "mlm_premasked": MLMPremaskedTask,
    "mlm_pretokenized": MLMPretokenizedTask,
    "mlqa": MlqaTask,
    "mnli": MnliTask,
    "mnli_mismatched": MnliMismatchedTask,
    "multirc": MultiRCTask,
    "mutual": MutualTask,
    "mutual_plus": MutualPlusTask,
    "mrpc": MrpcTask,
    "mrqa_natural_questions": MrqaNaturalQuestionsTask,
    "ner": NerTask,
    "newsqa": NewsQATask,
    "pawsx": PawsXTask,
    "panx": PanxTask,
    "pos": PosTask,
    "qamr": QAMRTask,
    "qasrl": QASRLTask,
    "qnli": QnliTask,
    "qqp": QqpTask,
    "quail": QuailTask,
    "quoref": QuorefTask,
    "race": RaceTask,
    "record": ReCoRDTask,
    "ropes": RopesTask,
    "rte": RteTask,
    "scitail": SciTailTask,
    "semeval": SemevalTask,
    "senteval_bigram_shift": SentEvalBigramShiftTask,
    "senteval_coordination_inversion": SentEvalCoordinationInversionTask,
    "senteval_obj_number": SentEvalObjNumberTask,
    "senteval_odd_man_out": SentEvalOddManOutTask,
    "senteval_past_present": SentEvalPastPresentTask,
    "senteval_sentence_length": SentEvalSentenceLengthTask,
    "senteval_subj_number": SentEvalSubjNumberTask,
    "senteval_top_constituents": SentEvalTopConstituentsTask,
    "senteval_tree_depth": SentEvalTreeDepthTask,
    "senteval_word_content": SentEvalWordContentTask,
    "snli": SnliTask,
    "socialiqa": SocialIQATask,
    "spr1": Spr1Task,
    "spr2": Spr2Task,
    "squad": SquadTask,
    "srl": SrlTask,
    "sst": SstTask,
    "stsb": StsbTask,
    "superglue_axb": SuperglueBroadcoverageDiagnosticsTask,
    "swag": SWAGTask,
    "tatoeba": TatoebaTask,
    "tydiqa": TyDiQATask,
    "udpos": UdposTask,
    "wic": WiCTask,
    "wnli": WnliTask,
    "wsc": WSCTask,
    "xnli": XnliTask,
    "xquad": XquadTask,
    "mcscript": MCScriptTask,
    "arct": ArctTask,
    "winogrande": WinograndeTask,
    "piqa": PiqaTask,
    # CAMeL
    "camel_pos": CAMeLposTask,
    "camel_prc3": CAMeLprc3Task,
    "camel_prc2": CAMeLprc2Task,
    "camel_prc1": CAMeLprc1Task,
    "camel_prc0": CAMeLprc0Task,
    "camel_per": CAMeLperTask,
    "camel_asp": CAMeLaspTask,
    "camel_vox": CAMeLvoxTask,
    "camel_mod": CAMeLmodTask,
    "camel_form_gen": CAMeLform_genTask,
    "camel_gen": CAMeLgenTask,
    "camel_form_num": CAMeLform_numTask,
    "camel_num": CAMeLnumTask,
    "camel_stt": CAMeLsttTask,
    "camel_cas": CAMeLcasTask,
    "camel_enc0": CAMeLenc0Task,
    "camel_rat": CAMeLratTask,
    # CAMeL combination
    "camel_cmb_per__gen__num": CAMeLper__gen__numTask,
    "camel_cmb_per__form_gen__form_num": CAMeLper__form_gen__form_numTask,
    "camel_cmb_asp__mod__vox": CAMeLasp__mod__voxTask,
    "camel_cmb_cas__stt": CAMeLcas__sttTask,
    "camel_cmb_prc3__prc2__prc1__prc0__enc0": CAMeLprc3__prc2__prc1__prc0__enc0Task,
    "camel_cmb_gen__num__rat": CAMeLgen__num__ratTask,
    "camel_cmb_pos__per__gen__num": CAMeLpos__per__gen__numTask,
    "camel_cmb_pos__per__form_gen__form_num": CAMeLpos__per__form_gen__form_numTask,
    "camel_cmb_pos__asp__mod__vox": CAMeLpos__asp__mod__voxTask,
    "camel_cmb_pos__cas__stt": CAMeLpos__cas__sttTask,
    "camel_cmb_pos__prc3__prc2__prc1__prc0__enc0": CAMeLpos__prc3__prc2__prc1__prc0__enc0Task,
    "camel_cmb_pos__gen__num__rat": CAMeLpos__gen__num__ratTask,
    "camel_cmb_per__gen__num__rat": CAMeLper__gen__num__ratTask,
    "camel_cmb_pos__per__gen__num__rat": CAMeLpos__per__gen__num__ratTask,
    "camel_cmb_tags17": CAMeLtags17Task,
    "camel_cmb_tags14": CAMeLtags14Task,
    # CAMeLGLF
    "camel_glf_pos": CAMeLGLFposTask,
    "camel_glf_prc3": CAMeLGLFprc3Task,
    "camel_glf_prc2": CAMeLGLFprc2Task,
    "camel_glf_prc1": CAMeLGLFprc1Task,
    "camel_glf_prc0": CAMeLGLFprc0Task,
    "camel_glf_per": CAMeLGLFperTask,
    "camel_glf_asp": CAMeLGLFaspTask,
    "camel_glf_vox": CAMeLGLFvoxTask,
    "camel_glf_mod": CAMeLGLFmodTask,
    "camel_glf_form_gen": CAMeLGLFform_genTask,
    "camel_glf_form_num": CAMeLGLFform_numTask,
    "camel_glf_stt": CAMeLGLFsttTask,
    "camel_glf_cas": CAMeLGLFcasTask,
    "camel_glf_enc0": CAMeLGLFenc0Task,
    "camel_glf_enc1": CAMeLGLFenc1Task,
    "camel_glf_enc2": CAMeLGLFenc2Task,
}


def get_task_class(task_name: str):
    task_class = TASK_DICT[task_name]
    assert issubclass(task_class, Task)
    return task_class


def create_task_from_config(config: dict, base_path: Optional[str] = None, verbose: bool = False):
    """Create task instance from task config.

    Args:
        config (Dict): task config map.
        base_path (str): if the path is not absolute, path is assumed to be relative to base_path.
        verbose (bool): True if task config should be printed during task creation.

    Returns:
        Task instance.

    """
    task_class = get_task_class(config["task"])
    for k in config["paths"].keys():
        path = config["paths"][k]
        # TODO: Refactor paths  (issue #1180)
        if isinstance(path, str) and not os.path.isabs(path):
            assert base_path
            config["paths"][k] = os.path.join(base_path, path)
    task_kwargs = config.get("kwargs", {})
    if verbose:
        print(task_class.__name__)
        for k, v in config["paths"].items():
            print(f"  [{k}]: {v}")
    # noinspection PyArgumentList
    return task_class(name=config["name"], path_dict=config["paths"], **task_kwargs)


def create_task_from_config_path(config_path: str, verbose: bool = False):
    """Creates task instance from task config filepath.

    Args:
        config_path (str): config filepath.
        verbose (bool): True if task config should be printed during task creation.

    Returns:
        Task instance.

    """
    return create_task_from_config(
        read_json(config_path), base_path=os.path.split(config_path)[0], verbose=verbose,
    )
