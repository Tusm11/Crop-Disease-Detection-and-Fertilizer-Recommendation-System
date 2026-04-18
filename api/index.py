from streamlit.web import cli as stcli
import sys
import os

# Set environment variables for Streamlit
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_PORT"] = "3000"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

def handler(request):
    """Vercel serverless function handler"""
    sys.argv = ["streamlit", "run", "app.py", "--logger.level=error"]
    stcli.main()
    return {"statusCode": 200}
