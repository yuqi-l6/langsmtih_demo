## setup
install packages using `pip install -r requirements.txt`
## connect to langsmith and trace
export the below in environment
You can put this in `.env` in the root dir
```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="<your-api-key>"
LANGSMITH_PROJECT="pr-drab-resolution-53"
OPENAI_API_KEY="<your-openai-api-key>"
```
