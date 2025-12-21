from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_API_KEY')
supabase: Client = create_client(url, key)

bancos = supabase.table('bancos').select('*').execute()
print(bancos)