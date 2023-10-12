import os
import subprocess
from textcleaner import TextCleaner
from gptsummarizer import GptSummarizer
from chunkssplitter import ChunksSplitter
import re
from fuzzywuzzy import fuzz
from chaptersidentifier import CHapterIdentifier
import fitz
from snapshotscreator import SnapshotsCreator
from FileWriter import FileWriter


class TextProcessor:
    global ROOT_DIR

    ROOT_DIR = os.path.abspath(os.curdir)

    def convert_pdf_to_txt(file_name):
        path = ROOT_DIR
        pdffname = f'{file_name}.pdf'
        txtfname = f'{file_name}.txt'

        subprocess.call(['pdftotext', '-simple',
                        os.path.join(path, pdffname),
                        os.path.join(path, txtfname)])

    def get_text_from_txt_file(file_name):
        with open(file_name) as f:
            contents = f.read()
        return contents

    def write_cleaned_text_to_file(file_name, text):

        file_name = f'{file_name} cleaned.txt'
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(text)

    def find_keyword_pages(file_name, keyword):
        keyword_pages = []

        path = ROOT_DIR
        pdffname = f'{file_name}.pdf'
        pdf_path = os.path.join(path, pdffname)

        pdf_document = fitz.open(pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            text = page.get_text()

            if keyword in text:
                # Add 1 to convert 0-based index to 1-based page number
                keyword_pages.append(page_number + 1)

        pdf_document.close()
        return keyword_pages

    def get_pages_images(file_name, start_page, end_page):

        for page in range(start_page, end_page+1):
            SnapshotsCreator.get_snapshot_of_page(
                file_name, page)

    def process_text(file_name):

        TextProcessor.convert_pdf_to_txt(file_name)

        text = TextProcessor.get_text_from_txt_file(f'{file_name}.txt')

        cleaned_text = TextCleaner.clean_text(text)

        TextProcessor.write_cleaned_text_to_file(file_name, cleaned_text)

        chapter_titles = CHapterIdentifier.identify_chapter_titles(
            cleaned_text)

        overview_chapter_text = CHapterIdentifier.extract_chapter_text(
            cleaned_text, chapter_titles, keywords=["Overview"])

        chunks = ChunksSplitter.split_text_to_chunks(overview_chapter_text)

        overview_summary = ""

        for chunk in chunks:

            summary_text = GptSummarizer.get_completion(chunk)

            overview_summary += f"{summary_text}\n"

        business_model_chapter_text = CHapterIdentifier.extract_chapter_text(
            cleaned_text, chapter_titles, keywords=["Business", "Model"])

        chunks = ChunksSplitter.split_text_to_chunks(
            business_model_chapter_text)

        business_model_summary = ""

        for chunk in chunks:

            summary_text = GptSummarizer.get_completion(chunk)

            business_model_summary += f"{summary_text}\n"

        financial_info_title_name = CHapterIdentifier.get_title_name_by_keywords(
            chapter_titles, keywords=["Financial", "information"])

        financial_info_title_page = TextProcessor.find_keyword_pages(
            file_name, financial_info_title_name)[0]

        financial_ratio_title_name = CHapterIdentifier.get_title_name_by_keywords(
            chapter_titles, keywords=["Financial", "ratio"])

        financial_ratio_title_page = TextProcessor.find_keyword_pages(
            file_name, financial_ratio_title_name)[0]

        TextProcessor.get_pages_images(
            file_name, financial_info_title_page, financial_ratio_title_page)

        risk_factor_summary = TextProcessor.get_risk_factors_summary_text(
            file_name)

        FileWriter.write_text_to_docx(
            file_name, overview_summary, business_model_summary, risk_factor_summary, financial_info_title_page, financial_ratio_title_page)

    def get_risk_factors_summary_text(company_name):

        file_name = f'{company_name} RF'
        TextProcessor.convert_pdf_to_txt(file_name)

        text = TextProcessor.get_text_from_txt_file(f'{file_name}.txt')

        cleaned_text = TextCleaner.clean_text(text)

        TextProcessor.write_cleaned_text_to_file(file_name, cleaned_text)

        chunks = ChunksSplitter.split_text_to_chunks(cleaned_text, 4000)

        risk_factors_summary = ""

        for chunk in chunks:

            summary_text = GptSummarizer.get_completion(chunk, 15)

            risk_factors_summary += f"{summary_text}\n\n"

        return risk_factors_summary


TextProcessor.process_text('Sunho Biologics')
