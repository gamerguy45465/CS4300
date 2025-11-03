from smolagents import ToolCallingAgent
import model_utils
from travel_agent.tools.web_tools import CityAttractionSearchTool, ScrapePageTool
from model import UniversityEventSearchTool, UniversitySearchEngineTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.google_build_reasoning_model()

    tools = [
        #CityAttractionSearchTool(),
        UniversityEventSearchTool(),
        UniversitySearchEngineTool(),
        ScrapePageTool(),
    ]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""You are an agent to help users by answering questions about Utah Tech University. When the user gives you a query asking you a
        question about something to do with the University, use UniversityEventSearchTool() to get the results already listed in a DataFrame. The results
        will be in a dictionary listed in the following format:
        
        {url: {title: description, ...}, ...}
         
        Use the dictionary to find the URL that matches the query. If no URL matches the query, then you will use the UniversitySearchEngineTool(), 
        which uses the DuckDuckGo search engine to get search results. The UniversitySearchEngineTool() will return the top results for the Query. 
        
        You will then use the results given from the UniversityEventSearchTool() or the UniversitySearchEngineTool(), to search for the URL that gives
        the results most relevant to the query.. You will then pass the result into ScrapePageTool(), which will give you the contents of that page.
        
        Afterwards, answer the users question with a Summary that is based on the contents that ScrapePageTool() gave you. Return your answer in a string
        format.
        """
    )
    return agent


