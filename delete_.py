







from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import requests
from decouple import config
import urllib3
from sqlalchemy.ext.declarative import declarative_base








# open working2.txt and not_working2.txt
with open("working2.txt", "w") as f:
    f.write(f"{'Working links File.':#^100}\n")
with open("not_working2.txt", "w") as f:
    f.write(f"{'Not Working Links File.':#^100}\n")

SQL_HOST = config('SQL_HOST', default='localhost')
SQL_USER = config('SQL_USER')
SQL_PASS = config('SQL_PASS')
SQL_DATABASE = config('SQL_DATABASE')

# create an engine to connect to the database
engine = create_engine(f'mysql://{SQL_USER}:{SQL_PASS}@{SQL_HOST}/{SQL_DATABASE}')



Base = declarative_base()
class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    link = Column(String)
Base.metadata.create_all(engine)




# create a session to execute queries
Session = sessionmaker(bind=engine)
session = Session()

# fetch all links from the database
results = session.query(Link.link).all()

print(f"{'Connected to database ready to check file.':#^100}")

with open("not_working.txt", "r") as f:
    not_working_links = f.readlines()
    not_working_links = [link.strip() for link in not_working_links]

# fetch the links from the database that are in the not_working_links list
results = session.query(Link).filter(Link.link.in_(not_working_links)).all()

if results:
    print("These are the first 10 links that will be deleted:")
    for i, link in enumerate(results[:10]):
        print(f"{i+1}. http://{link.link}")
    confirm = input("Are you sure you want to delete these links from the database? (y/n) ")
    if confirm.lower() == "y":
        for link in results:
            session.delete(link)
        session.commit()
        print("Links have been deleted from the database.")
    else:
        print("Links were not deleted from the database.")
else:
    print("No matching links were found in the database.")
