import pandas as pd
import numpy as np


def start_pandas():
    df = pd.read_csv("events.csv")
    dates = np.array(df["date"])
    start_times = np.array(df["start_time"])
    end_times = np.array(df["end_time"])
    titles = np.array(df["title"])
    locations = np.array(df["location"])
    categories = np.array(df["category"])
    descriptions = np.array(df["description"])
    urls = np.array(df["url"])

    return dates, start_times, end_times, titles, locations, descriptions, urls, categories






dates, start_times, end_times, titles, locations, descriptions, urls, categories = start_pandas()

print(dates)
print(start_times)
print(end_times)
print(titles)
print(locations)
print(descriptions)
print(urls)
print(categories)