

import os
import streamlit as st
@st.cache_resource
def init_connection1():
	return os.system("""/home/adminuser/venv/bin/python copy_poll.py > log-bb-file.txt""")
_=init_connection1()
#STREAMLIT SITE
#/home/adminuser/venv/bin/.py & /home/adminuser/venv/bin/python bb.py")
#import os
#os.system("""/home/adminuser/venv/bin/python soojh.py & /home/adminuser/venv/bin/python aa.py & /home/adminuser/venv/bin/python bb.py""")
#/home/adminuser/venv/bin/python -m pip install --upgrade pip & 
#/home/adminuser/venv/bin/python multi-acc.py & 