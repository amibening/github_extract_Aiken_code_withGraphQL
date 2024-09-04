import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv

# prerequisites -  pip install requests-toolbelt, pip install python-dotenv
# Set up config.env and add to gitignore file as contains GITHUB_ACCESS_TOKEN

# Specify the path to your config.env file
dotenv_path = 'config.env'

# Load environment variables from the config.env file
load_dotenv(dotenv_path)

# Fetch the GitHub access token from environment variables
github_token = os.getenv("GITHUB_ACCESS_TOKEN")

if not github_token:
    raise ValueError('GITHUB_ACCESS_TOKEN environment variable not set')

# Set up the GraphQL transport (API endpoint and headers)
transport = RequestsHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": f"Bearer {github_token}"},
    use_json=True,
)

# Initialize the client
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GitHub search query
github_query = "NOT fork:true path:*.ak Aiken"

# Define how many results to return
num_results = 10  # Set this to the number of repositories you want to fetch

# Construct the GraphQL query by dynamically injecting the search query and number of results
graphql_query = gql(f"""
{{
  search(query: "{github_query}", type: REPOSITORY, first: {num_results}) {{
    edges {{
      node {{
        ... on Repository {{
          name
          owner {{
            login
          }}
          description
          isFork
          url
        }}
      }}
    }}
  }}
}}
""")

# Execute the query
try:
    result = client.execute(graphql_query)

    # Print the results
    for repo in result['search']['edges']:
        repo_node = repo['node']
        print(f"Repository: {repo_node['name']}")
        print(f"Owner: {repo_node['owner']['login']}")
        print(f"Description: {repo_node.get('description', 'No description')}")
        print(f"Is Fork: {repo_node['isFork']}")
        print(f"URL: {repo_node['url']}\n")

except Exception as e:
    print(f"Error: {e}")
