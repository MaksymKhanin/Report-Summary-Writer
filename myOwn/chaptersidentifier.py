import re


class CHapterIdentifier:

    def identify_chapter_titles(text):
        pattern = r'\n\s*([A-Z][a-zA-Z]+(?: [a-zA-Z]+)*?[^\s\.:])\n\n'
        chapter_titles = re.findall(pattern, text)
        return chapter_titles

    def extract_text(text, start_title, chapter_titles):
        start_index = chapter_titles.index(start_title)
        if start_index < len(chapter_titles) - 1:
            end_title = chapter_titles[start_index + 1]
            pattern = r'\n\s*(' + re.escape(start_title) + \
                r')\n\n(.*?)\n\s*' + re.escape(end_title) + r'\n\n'
            chapter_text = re.search(
                pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if chapter_text:
                return chapter_text.group(2).strip()
        return None

    def are_keywords_in_title(title, keywords):
        for keyword in keywords:
            if keyword.lower() not in title.lower():
                return False
        return True

    def get_title_name_by_keywords(titles, keywords):
        for title in titles:
            if CHapterIdentifier.are_keywords_in_title(title, keywords):
                return title
        return None

    def extract_chapter_text(text, chapter_titles, keywords):
        chapter_texts = {}
        for title in chapter_titles:
            if CHapterIdentifier.are_keywords_in_title(title, keywords):
                chapter_text = CHapterIdentifier.extract_text(
                    text, title, chapter_titles)

        return chapter_text
