#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import pandas as pd
import vincent

all_data = open("Data/running-times.list").readlines()[15:-2]
# print len(all_data)

parsed_data = []

for line in all_data:
    release_date = re.search(r'(\d\d\d\d)', line)
    run_time = re.search(r'\d+[\t\n]', line)
    # movie_title = re.search(r'[#!$?.\'\s\w]+', line)
    # if movie_title and release_date and run_time is not None:
    #     parsed_data.append([movie_title.group(), int(release_date.group()), int(run_time.group().strip())])
    if release_date and run_time is not None:
        parsed_data.append([int(release_date.group()), int(run_time.group().strip())])
    else:
        pass

# Filter out TV shows (if divisible by 30)
parsed_films = filter(lambda x: x[1] % 30, parsed_data)

# Pandas DataFrame
films = pd.DataFrame(parsed_films)
filtered_films = films[(films[0] > 1920) & (films[0] < 2015) & (films[1] > 45)]
# print filtered_films.describe()

films_by_year = filtered_films.groupby(0).mean()

line = vincent.Line(films_by_year)
line.axis_titles(x='Year', y="Run time")
line.to_json('movies.json', html_out=True, html_path='movies_template.html')

# Note to view movies_template.html locally, start and http server with:
# $python -m SimpleHTTPServer 8000
# And then visit: http://localhost:8000
