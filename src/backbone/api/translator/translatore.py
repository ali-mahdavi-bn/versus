import json
import os
from pathlib import Path

current_dir = os.path.dirname(__file__)
root_path_ = Path(current_dir).parent.parent.absolute()

dict_translate = {
    "message": {
        "fa": json.loads(Path(root_path_.joinpath(f'apis/translator/phrases/message/fa.json')).read_text(
            encoding="utf-8"))
    },
    "error": {
        "fa": json.loads(Path(root_path_.joinpath(f'apis/translator/phrases/error/fa.json')).read_text(
            encoding="utf-8"))
    },
}


def _get_lan(type, lan='fa'):
    json_load = json.loads(Path(root_path_.joinpath(f'apis/translator/phrases/{type}/{lan}.json')).read_text(
        encoding="utf-8"))
    return json_load


def translate(*, phraseMessage, type="error", lan='fa'):
    if parse_translate := dict_translate.get(type).get(lan):
        return parse_translate

    lan = _get_lan(type, lan=lan)
    return lan[phraseMessage]
