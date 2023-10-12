import camelot
from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# reads the table from pdf file

# # df = read_pdf("Sunho Biologics.pdf", pages="all")  # address of pdf file
# tables = read_pdf("Sunho Biologics.pdf",
#                   pages="all", multiple_tables=True)


# with open("Sunho Biologics Tables Only", 'w', encoding="utf-8") as f:
#     f.write("")

# for table in tables:
#     with open("Sunho Biologics Tables Only", 'a', encoding="utf-8") as f:
#         dfAsString = table.to_string(header=True, index=True)
#         f.write(dfAsString)


# print(tabulate(df))


tables = camelot.read_pdf("Sunho Biologics.pdf",
                          pages='all', flavor='stream')

with open("Sunho Biologics Tables Only", 'w', encoding="utf-8") as f:
    f.write("")


for table in tables:
    with open("Sunho Biologics Tables Only", 'a', encoding="utf-8") as f:
        dfAsString = table.df.to_string(header=True, index=True)
        f.writelines(" ")
        f.write(dfAsString)
