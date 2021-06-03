# twitter-nba-network-analysis
simple network analysis of NBA players using Twitter's API. The data and results are based on data as of __June 12, 2020__ 

## Some background knowledge which will help
1. Basic-intermediate Python knowledge
2. Basics of Networks/Graphs: directed graphs/degree centrality/betweenness centrality/etc
3. making REST requests (in Python) to external APIs (in this case, Twitter)
4. Basic knowledge of how to do network visualizations in __Gephi__

## Installation 
1. Obtain an API key, Consumer Key, and Bearer Token, following instructions from [Twitter's developer guide](https://developer.twitter.com/en/docs/basics/getting-started).
2. Clone this repository.
3. Create a directory named `app_secrets` in the project repository
4. in the `app_secrets` directory, create a python file named `secrets.py`. Inside this file, add your keys and bearer token from step 1. Simply store the values as strings. For example, `BEARER_TOKEN = {YOUR_BEARER_TOKEN}`
5. Install [Gephi](https://gephi.org/users/install/). This software is what was used for the network visualizations
6. Open the scripts `data_fetching_scripts.py` and `data_analysis.py` in the `src/data` directory, and ensure you have the necessary python packages e.g requests, pandas, matplotlib, etc

## Running code / Obtaining data
- Run the script in `src/data/data_fetching_scripts.py`
- Note: The script above will take __hours__ to run. This is because of [Twitter's standard API restrictions](https://developer.twitter.com/en/docs/basics/rate-limiting). To obtain your data, you could run the script overnight
- Feel free to modify the script/functions, but pay close attention to the code comments to understand how I did my implementation
- load up your nodes and edge list csv files in Gephi and do any analysis you want
- Use the script in `src/data_analysis.py` to see how to use the data to create math plots or or analyze the graph as a networkx graph
- _My own csv files have not been committed. Running the scripts will help you generate yours. However, you can also load up the file 
in `src/data/gephiprojectnbanetworkanalysis.graphml.gephi` in gephi. It is a gephi project which contains some analysis I did_


## Insights
- I have included some of my results/visualizations in the `src/data/visualizations` directory
- See my [Medium article](https://medium.com/@h.ogeleka/social-network-analysis-of-current-nba-players-on-twitter-b3fb9a741806) for a discussion on this project and its results

