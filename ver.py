import pydantic.version
import sqlalchemy
import pydantic
import fastapi
import database

print(sqlalchemy.__version__)
print(pydantic.version)
print(fastapi.__version__)

# output:
# 2.0.38
# <module 'pydantic.version' from 'C:\\studies\\codemain\\fastapi\\env\\Lib\\site-packages\\pydantic\\version.cp312-win_amd64.pyd'>
# 0.115.8