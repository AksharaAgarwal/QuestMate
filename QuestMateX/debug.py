#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:\\Users\\MY DELL\\Desktop\\Akshara\\QuestMateX')

try:
    import app
    print("App imported successfully!")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
