import re


class TextCleaner:

    def find_paragraph(text, start_phrase, end_phrase):
        pattern = re.escape(start_phrase) + r".*?" + re.escape(end_phrase)
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            paragraph = match.group(0)
            print("Found paragraph:")
            print(paragraph)
            return paragraph

        else:
            print("Paragraph not found.")
            return None

    def remove_brackets(text):
        text = text.replace('[', '')
        text = text.replace(']', '')
        return text

    def remove_headers(text):
        paragraph = TextCleaner.find_paragraph(
            text, "This summary aims", "decide to REDACTED in the REDACTED.")

        if paragraph is not None:
            text = text.replace(paragraph, '')

        paragraph = TextCleaner.find_paragraph(
            text, "This document is in", "ON THE COVER OF THIS DOCUMENT")

        if paragraph is not None:
            text = text.replace(paragraph, '')

        paragraph = TextCleaner.find_paragraph(
            text, "THERE IS NO ASSURANCE", "PRODUCTS SUCCESSFULLY.")

        if paragraph is not None:
            text = text.replace(paragraph, '')

        return text

    def remove_page_numbers(text):
        patterns = [
            r"(?:\s*[-–—]\s*\d+\s*[-–—]\s*)",
            r"(?:\s*[-–—]\s*\d+\s*[-–—]\s*\n)"
        ]

        for pattern in patterns:
            text = re.sub(pattern, '', text)

        return text

    def remove_summary(text):

        summary1 = "SUMMARY\n"
        summary2 = "SUMMARY"

        text = text.replace(summary1, '')
        text = text.replace(summary2, '')
        return text

    def remove_multiple_empty_lines(text, threshold=3):
        pattern = r'\n\s{' + str(threshold) + ',}\n'
        cleaned_text = re.sub(pattern, '\n\n', text)
        return cleaned_text

    def clean_text(text):

        text = TextCleaner.remove_brackets(text)
        text = TextCleaner.remove_headers(text)
        text = TextCleaner.remove_page_numbers(text)
        text = TextCleaner.remove_summary(text)
        text = text.replace("", '')
        text = TextCleaner.remove_multiple_empty_lines(text)

        return text
