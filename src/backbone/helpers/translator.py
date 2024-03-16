from googletrans import Translator as translator_moduls


class Translator:
    def __init__(self):
        print('Translator_')
        self._translator = translator_moduls()

    def _translate_to_farsi(self, text, language='fa'):
        translator = self._translator
        translation = translator.translate(text, src='en', dest=language) if text.strip() else ""
        return translation.text if translation != "" else ""

    def translate(self, text, language='fa'):
        if text:
            return self._translate_to_farsi(text, language)

    def _split_text(self, text, max_chars=5000):
        paragraphs = text.split('\n')

        self._current_paragraph = ''
        self._result = []

        for paragraph in paragraphs:
            if len(self._current_paragraph) + len(paragraph) <= max_chars:
                self._current_paragraph += paragraph + '\n'
            else:
                self._result.append(self._current_paragraph.strip())
                self._current_paragraph = paragraph
        if self._current_paragraph.strip():
            self._result.append(self._current_paragraph.strip())

        return self._result

    def translating_long_text(self, text=""):
        try:
            text_splits = self._split_text(text)
            translated_text = ''.join((self._translate_to_farsi(text_split) for text_split in text_splits))
        except Exception as e:
            print(f"Error translating text: {e}")
            translated_text = ""

        return translated_text


