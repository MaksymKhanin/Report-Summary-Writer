from pdf2image import convert_from_path


class SnapshotsCreator:

    def get_snapshot_of_page(file_name, page_number):
        pages = convert_from_path(f'{file_name}.pdf', 500)

        for count, page in enumerate(pages):
            if count == (page_number-1):
                page.save(f'{file_name} {page_number}.png', 'JPEG')
