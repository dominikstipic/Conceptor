import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import numpy as np

def sort_dict_by_value(ds):
    return dict(sorted(ds.items(), key=lambda item: item[1]))

def get_startup_data():
    link = "https://www.eu-startups.com/directory"
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    extracted = soup.find("div", id="wpbdp-categories")
    lists = extracted.find_all("li")
    countries = [l.text.strip().split() for l in lists if l != None]
    countries = [[k, int(v[1:-1])]for k,v in countries]
    countries = dict(countries)
    labels = list(countries.keys())
    values = list(countries.values())
    ds = dict(zip(labels, values))
    ds = sort_dict_by_value(ds)
    return ds


def create_fig(ds):
    fig, ax = plt.subplots()
    keys, values = list(ds.keys()), list(ds.values())
    ax.bar(keys, values)
    ax.set_title('Startups in EU')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Frequency')
    ax.tick_params(axis='x', labelrotation=90, which='major', length=1, width=1, labelsize=7)
    ax.grid(True)
    for i, v in enumerate(values):
        ax.text(i, v + 200, str(v), ha='center', fontsize=8)
    return fig, ax

def get_startup_data_by_ratio():
    startups = get_startup_data()
    with open('population.json', 'r') as f: 
        population = json.load(f)
    result = {}
    for k in startups:
        result[k] = float(np.round(-np.log(startups[k] / population[k]), 3))
    result = sort_dict_by_value(result)
    return result

def get_data(by_ratio):
    if not by_ratio: 
        fig, ax = create_fig(get_startup_data())
    else:
        fig, ax = create_fig(get_startup_data_by_ratio())
    return fig, ax

