import os
from supabase import create_client

SUPABASE_URL = "https://qkprheovahmesredgjkv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrcHJoZW92YWhtZXNyZWRnamt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyMTcwMjMsImV4cCI6MjA1NTc5MzAyM30.34WmlTpgoOg1o4pqes5xleKtp_IJYQrZDPPewutx934"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
