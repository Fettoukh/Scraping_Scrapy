# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector as connector
from itemadapter import ItemAdapter


class JobmarketPipeline:
    spider=None
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        self.conn=connector.connect(
            host='localhost',
            user='root',
            passwd='1234',
            database='prospective-emploi'
        )
        self.curr=self.conn.cursor()


    def process_item(self, item, spider):
        self.spider=spider
        items=item
        name= self.spider.name
        self.store_db(items)
        print("\n--------------------------------------------------")
        print("Pipeline: "+ name+"\n nb_poste:"+ items['Nb_poste'])
        print("\n---------------------------------------------------")
        return item

    def store_db(self,item):
        description=item['desc_poste']+"\n------description profil---------------"+ item['desc_profile']
        self.curr.execute("""insert into pre_normalized_offre_emploi values(NULL,%s,%s,%s,%s,%s,%s,%s,%s)""",(
        int(item['Nb_poste']),
        item['Entreprise'],
        item['Secteur'],
        item['Metier'] ,
        item['Date'] ,
        item['Region'] ,
        description,
        self.spider.name
         )    )
        self.conn.commit()