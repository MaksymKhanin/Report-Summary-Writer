from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PyPDF2 import PdfReader, PdfWriter
from textsummarizer import TextSummarizer
import io
import re
import os

WEBPAGE_URI_TO_SCRAPE = 'https://www1.hkexnews.hk/app/appindex.html'
FIRST_DATA_FRAME_COLUMN = "Latest Posting Date"
SECOND_DATA_FRAME_COLUMN = "Applicants"
COMMON_URI = "https://www1.hkexnews.hk/app/"

_chrome_driver = webdriver.Chrome()


def concatenate_url(uri):
    full_uri = COMMON_URI + uri
    return full_uri


# remove this method
def parse_all_pdf_links_from_dataframe(data_frame):

    data_frame = data_frame.reset_index()
    for index, row in data_frame.iterrows():
        pdf_uri = concatenate_url(row['Link1'])
        # Get response object for link
        r = requests.get(pdf_uri)
        f = io.BytesIO(r.content)
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        count = 0
        full_pdf = ''
        for index in reader.pages:
            full_pdf += reader.pages[count].extract_text()


def get_and_append_summary_pdf_from_dataframe(data_frame):
    pdf_links = dict()

    data_frame = data_frame.reset_index()
    full_summary_pdf_link = ''
    for index, row in data_frame.iterrows():
        full_htm_uri = concatenate_url(row['Htm_Link1'])

        split_link = x = row['Htm_Link1'].split("/")
        uri_middle_part = f'{split_link[0]}/{split_link[1]}/{split_link[2]}/'

        company_name = extract_company_name(row['Applicants'])
        posting_date = row['Latest Posting Date']

        html_page_source = get_html_page_from_uri(full_htm_uri)

        in_memory_list_of_scraped_table = get_pdfs_from_htm(
            html_page_source)

        summary_and_risk_factors_pdf_links = []

        for row in in_memory_list_of_scraped_table:

            if 'SUMMARY' in row or 'Summary' in row:
                summary_pdf_link = row[2]
                partial_pdf_uri = uri_middle_part + summary_pdf_link
                full_summary_pdf_link = concatenate_url(partial_pdf_uri)

                summary_and_risk_factors_pdf_links.append(
                    full_summary_pdf_link)

            if 'RISK FACTORS' in row or 'Risk Factors' in row or 'Risk factors' in row or 'risk' in row:
                risk_factors_pdf_link = row[2]
                partial_pdf_uri = uri_middle_part + risk_factors_pdf_link
                full_risk_factors_pdf_link = concatenate_url(partial_pdf_uri)

                summary_and_risk_factors_pdf_links.append(
                    full_risk_factors_pdf_link)

        if company_name not in pdf_links.keys():
            pdf_links[company_name] = summary_and_risk_factors_pdf_links

    return pdf_links


def extract_company_name(text):
    pattern = r"Applicant:\s+(.*?)\d{2}/\d{2}/\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def get_pdfs_from_htm(html_page_source):
    soup = BeautifulSoup(html_page_source, "html.parser")

    in_memory_list_of_scraped_pdf_links = []

    tables = soup.find_all('table')
    table = tables[2]
    table_rows = table.find_all('tr')

    for tr in table_rows:
        table_data = tr.find_all('td')
        row = [tr.text.strip() for tr in table_data if tr.text.strip()]
        for data in table_data:
            anchors = data.find_all('a')
            for anchor in anchors:
                a_href = anchor.get('href')
                if a_href:
                    if '.pdf' in a_href:
                        row.append(a_href)

        if row:
            in_memory_list_of_scraped_pdf_links.append(row)

    return in_memory_list_of_scraped_pdf_links


def scrape_table_with_soup(html_page_source):
    soup = BeautifulSoup(html_page_source, "html.parser")

    table = soup.find('table')
    table_rows = table.find_all('tr')

    in_memory_list_of_scraped_table = []

    for tr in table_rows:
        table_data = tr.find_all('td')
        row = [tr.text.strip() for tr in table_data if tr.text.strip()]
        for data in table_data:
            anchors = data.find_all('a')
            for anchor in anchors:
                a_href = anchor.get('href')
                if a_href:
                    if '.htm' in a_href:
                        row.append(a_href)

        if row:
            in_memory_list_of_scraped_table.append(row)

    return in_memory_list_of_scraped_table


def index_data_to_dataframe(index_page_data_list):

    data_frame = pd.DataFrame()

    if len(index_page_data_list) > 0:
        longest = max(index_page_data_list, key=len)
        columns = [FIRST_DATA_FRAME_COLUMN, SECOND_DATA_FRAME_COLUMN]

        counter = 1
        for elem in longest[2:]:
            columns.append(f'Htm_Link{counter}')
            counter += 1

        data_frame = convert_list_to_dataframe(
            index_page_data_list, columns)

        # pd.set_option('display.max_columns', None)

    return data_frame


def convert_list_to_dataframe(input_collection, dataframe_columns):
    data_frame = pd.DataFrame()
    data_frame = pd.DataFrame(
        input_collection, columns=dataframe_columns)
    return data_frame


def convert_dict_to_dataframe(input_collection, dataframe_columns):
    data_frame = pd.DataFrame()
    data_frame = pd.DataFrame.from_dict(
        input_collection, orient='index')
    data_frame.columns = dataframe_columns
    return data_frame


def get_html_page_from_uri(webpage_uri):

    _chrome_driver.get(webpage_uri)
    html_page_source = _chrome_driver.page_source

    return html_page_source


def read_pdf_link_text(pdf_link):
    text = ''
    r = requests.get(pdf_link)
    f = io.BytesIO(r.content)
    reader = PdfReader(f)
    num_pages = len(reader.pages)

    count = 0
    for index in reader.pages:
        text += reader.pages[count].extract_text()
        count += 1

    return text


def write_summary_from_dict_to_files(summary_pdf_links_dictionary):
    text_summarizations_list = []
    for key, value in summary_pdf_links_dictionary.items():
        text = read_pdf_link_text(value)

        # get topic from text
        text_summarization = extract_topic_from_text(text)
        text_summarization = " "
        text_summarizations_list.append(text_summarization)

        print(text)
        split_key = key.split(" ")
        file_name = f'{split_key[1]} {split_key[2]} {split_key[3]}.txt'
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(text)

        # summaey_file_name = f'{split_key[1]} {split_key[2]} {split_key[3]} Summary.txt'
        # with open(summaey_file_name, 'w', encoding="utf-8") as f:
        #     f.write(text_summarization)


def extract_topic_from_text(text):
    text_summarization = TextSummarizer.get_summary_from_text(text)
    return text_summarization


def create_folder(folder_name):
    root_path = os.getcwd()  # Get the current working directory
    new_folder_path = os.path.join(root_path, folder_name)

    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)

    return new_folder_path


def download_pdf(pdf_url, folder_path, file_name):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_path = os.path.join(folder_path, file_name)
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)


def save_pdf_files_to_folder(company_name, summary_pdf_link, risk_factors_pdf_link):
    if company_name and summary_pdf_link and risk_factors_pdf_link:
        folder_path = create_folder(company_name)
        download_pdf(summary_pdf_link, folder_path, f'{company_name}.pdf')
        download_pdf(risk_factors_pdf_link, folder_path,
                     f'{company_name} RF.pdf')


def main():

    html_page_source = get_html_page_from_uri(WEBPAGE_URI_TO_SCRAPE)

    index_page_data = scrape_table_with_soup(html_page_source)

    data_frame = index_data_to_dataframe(index_page_data)

    print(data_frame)

    summary_pdf_links_dictionary = get_and_append_summary_pdf_from_dataframe(
        data_frame)

    columns = ['Summary pdf link', 'Risk Factors pdf link']
    pdf_links_dataframe = convert_dict_to_dataframe(
        summary_pdf_links_dictionary, columns)

    for key, values in summary_pdf_links_dictionary.items():
        value1, value2 = values
        company_name = key
        summary_pdf_link = value1
        risk_factors_pdf_link = value2
        save_pdf_files_to_folder(
            company_name, summary_pdf_link, risk_factors_pdf_link)

    _chrome_driver.quit()


main()
