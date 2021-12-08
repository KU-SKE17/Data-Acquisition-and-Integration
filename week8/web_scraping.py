import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.settrade.com/C13_MarketSummary.jsp")
soup = BeautifulSoup(response.text, "html.parser")

# # extract indices; also strip out wrapping whitespaces
# indices = [s.text.strip() for s in soup.select(".col-md-8 a")]

# # extract values; get rid of ',' and convert to numbers
# values = [
#     float(s.text.replace(",", ""))
#     for s in soup.select(".col-md-8 td:nth-of-type(2)")
# ]

# for idx, val in zip(indices, values):
#     print(f"{idx} : {val}")

values = soup.select(".col-md-8 td:nth-of-type(2)")
print(values) 
# [<td>1,616.82</td>, <td>962.16</td>, <td>2,202.34</td>, <td>1,062.27</td>, <td>1,019.87</td>, <td>1,128.36</td>, <td>1,012.94</td>, <td>943.35</td>, <td>567.99</td>]

values = [
    float(s.text.replace(",", ""))
    for s in soup.select(".col-md-8 td:nth-of-type(2)")
]
print(values) 
# [1616.85, 962.34, 2202.54, 1062.17, 1020.04, 1128.39, 1013.19, 943.52, 567.29]