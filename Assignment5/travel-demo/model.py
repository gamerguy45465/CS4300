from smolagents import Tool, DuckDuckGoSearchTool
import pandas as pd
import numpy as np


class UniversityEventSearchTool(Tool):
    name = "university_event_search"
    description = """Given a Pandas DataFrame that contains information about Utah Tech University, and given the name of an event,
    this tool will return the results from that DataFrame. The results will be stored in a Python Dictionary of the following form:
    
    {url: {title: description, ...}, ...}
    
    """
    inputs = {"query": {"type": "string", "description": "Event name to search for"}}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv("events.csv")

    def forward(self, query: str) -> str:
        urls = list(self.df["url"])
        titles = list(self.df["title"])
        descs = list(self.df["description"])
        url_title = {}

        for i in range(len(urls)):
            td = {titles[i]: descs[i]}
            url_title[urls[i]] = td


        return str(url_title)



class UniversitySearchEngineTool(Tool):
    name = "university_search"
    description = "Given a query, this tool will return the results from that query"
    inputs = {"query": {"type": "string", "description": "The query to search for."}}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self._ddgs = DuckDuckGoSearchTool()

    def forward(self, query: str) -> str:
        if not query:
            return "Error: no query provided."
        result = self._ddgs(query)
        return result



