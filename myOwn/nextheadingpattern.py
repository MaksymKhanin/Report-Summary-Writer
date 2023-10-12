import re

text = """
Our Business Model

      Our core business model involves internally discovering, developing and
commercializing immunocytokines and other immunotherapies to address unmet needs in the
fields of oncology and autoimmune diseases. We also recognize that partnerships will be a
critical source to complement our internal resource and enable us to fully execute our global
strategy. As such, we will actively seek collaboration opportunities with international leading
pharmaceutical companies to advance clinical studies of our products abroad through
out-licensing arrangements. We will also expand our international registration team to
coordinate with KOLs and FDA regulation specialists to secure our global clinical development
and registration plan, and strengthen the leading position of our featured products, especially
our immunocytokine pipeline products including IAP0971, IAE0972 and IBB0979.

                                                          -4-
THIS DOCUMENT IS IN DRAFT FORM, INCOMPLETE AND SUBJECT TO CHANGE AND THAT THE INFORMATION MUST
BE READ IN CONJUNCTION WITH THE SECTION HEADED "WARNING" ON THE COVER OF THIS DOCUMENT

                                           SUMMARY

Our Pipeline

      Our pipeline includes three Core Products: two immunocytokines and one ADCC
enhanced mAb. The two immunocytokines, IAP0971 and IAE0972, were developed based on
our AICTM platform. The ADCC enhanced mAb, IAH0968, was developed based on our
AEATM Platform. The following chart summarizes the development status of our Core
Products and other selected product candidates as of the Latest Practicable Date.
"""

start_pattern = re.compile(r'OUR BUSINESS MODEL\n(.*?)\n', re.IGNORECASE)

# Find the start of the "Our business model" chapter
start_match = start_pattern.search(text)

if start_match:
    start_position = start_match.end()

    # Find the next heading to determine the end of the chapter
    next_heading_pattern = re.compile(r'\n([^#\n].*?)\n', re.DOTALL)
    next_heading_match = next_heading_pattern.search(text[start_position:])

    if next_heading_match:
        end_position = start_position + next_heading_match.start()
    else:
        end_position = len(text)

    business_model_chapter = text[start_position:end_position].strip()
    print(business_model_chapter)
else:
    print("Chapter not found.")
