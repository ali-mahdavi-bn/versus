import json
from typing import List
from uuid import uuid4

from backbone.crawler.helper.helpers.response import Response


class ContentPage(str):
    pass


class DetailPage(dict):
    pass


class CategoryDTO:
    def __init__(self, slug, name, icon, picture, langs, categories):
        uuid = uuid4()
        self.uuid = uuid
        self.slug = slug
        self.name = name
        self.icon = icon
        self.picture = picture
        self.langs = langs
        self.categories = [SubCategory(sub_category_uuid=uuid, **cat) for cat in categories]


class SubCategory:
    def __init__(self, sub_category_uuid, name, name_url):
        self.sub = sub_category_uuid
        self.name = name
        self.name_url = name_url


def clear_page_category_verses(response: Response) -> List[CategoryDTO]:
    second_script_content = response.css('script#reactInitData').get()
    content = extract_data(second_script_content)
    return process_data(content=content)


def extract_data(content: ContentPage) -> ContentPage:
    start_index: int = content.find('={') + 1 if content else 0
    end_index: int = content.find('</script>') if content else 0
    return content[start_index:end_index] if start_index else ""


def process_data(content: ContentPage) -> List[CategoryDTO]:
    start = "\"catGroups\""
    start = content.find(start)
    end = "\"dealSettings\""
    end = content.find(end)
    content_ = "{" + content[start:end - 1] + "}"

    data: DetailPage = json.loads(content_.replace("undefined", "\"\"").replace("\'", "").strip())
    category_groups: List[CategoryDTO] = get_category_groups(data)
    return category_groups


def get_category_groups(data: DetailPage) -> List[CategoryDTO]:
    categories = data.get("catGroups")
    return [CategoryDTO(**category) for category in categories]
