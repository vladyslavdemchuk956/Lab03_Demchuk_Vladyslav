import re
import subprocess
import sys

import matplotlib
import nbformat
from nbclient import NotebookClient

matplotlib.use("Agg")

quarto = sys.argv[1] if len(sys.argv) > 1 else "quarto"
subprocess.run([quarto, "convert", "report.qmd", "-o", "report.ipynb"], check=True)

nb = nbformat.read("report.ipynb", as_version=4)

namespace = {}
for cell in nb.cells:
    if cell.cell_type == "code":
        exec(cell.source, namespace)

citations = {
    "[-@chu2001]": "(2001)",
    "[-@scott2010]": "(2010)",
    "[-@r4ds]": "(2017)",
    "[@scott2010]": "(Scott, Yelowitz, 2010)",
    "[@ggplot2]": "(Wickham, 2016)",
    "[@duan1983]": "(Duan, 1983)",
}
references = """**Бібліографія**

- Chu S. Pricing the C's of Diamond Stones // Journal of Statistics Education. 2001. Vol. 9, No. 2. https://jse.amstat.org/v9n2/datasets.chu.html
- Duan N. Smearing Estimate: A Nonparametric Retransformation Method // JASA. 1983. Vol. 78, No. 383. P. 605–610. https://doi.org/10.1080/01621459.1983.10478017
- James G., Witten D., Hastie T., Tibshirani R., Taylor J. An Introduction to Statistical Learning with Applications in Python. Springer, 2023. https://doi.org/10.1007/978-3-031-38747-0
- Kuhn M., Silge J. Tidy Modeling with R. O'Reilly, 2022. https://www.tmwr.org/
- NIST/SEMATECH. e-Handbook of Statistical Methods: How can I tell if a model fits my data? https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm
- Sandve G. K. et al. Ten Simple Rules for Reproducible Computational Research // PLoS Computational Biology. 2013. Vol. 9, No. 10. https://doi.org/10.1371/journal.pcbi.1003285
- Scott F., Yelowitz A. Pricing Anomalies in the Market for Diamonds: Evidence of Conformist Behavior // Economic Inquiry. 2010. Vol. 48, No. 2. P. 353–368. https://doi.org/10.1111/j.1465-7295.2009.00237.x
- Wickham H. ggplot2: Elegant Graphics for Data Analysis. Springer, 2016. https://doi.org/10.1007/978-3-319-24277-4
- Wickham H., Grolemund G. R for Data Science. O'Reilly, 2017. https://r4ds.had.co.nz/
"""


def fill_inline(match):
    return str(eval(match.group(1), namespace))


for cell in nb.cells:
    if cell.cell_type == "raw" or cell.source.startswith("---"):
        cell.cell_type = "markdown"
        cell.pop("outputs", None)
        cell.pop("execution_count", None)
        cell.source = ("# Від чого залежить ціна діаманта: регресійне моделювання\n\n"
                       "**Лабораторна робота №3. Основи регресійного моделювання**\n\n"
                       "Демчук Владислав")
        continue
    if cell.cell_type != "markdown":
        continue
    text = cell.source
    text = re.sub(r"`\{python\} (.+?)`", fill_inline, text)
    for key, value in citations.items():
        text = text.replace(key, value)
    text = re.sub(r"@fig-[\w-]+", "графік вище", text)
    text = re.sub(r"@tbl-[\w-]+", "таблиця нижче", text)
    text = text.replace("::: {.callout-warning}\n", "> **Увага.** ")
    text = text.replace(" {.unnumbered}", "")
    text = text.replace("::: {#refs}\n:::", references)
    text = text.replace("\n:::", "")
    cell.source = text

client = NotebookClient(nb, timeout=600, kernel_name="python3")
client.execute()
nbformat.write(nb, "report.ipynb")
print("report.ipynb готовий")
