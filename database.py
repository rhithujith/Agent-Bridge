import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Provide fallback values to prevent server crash if .env is not yet configured
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-anon-key")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
