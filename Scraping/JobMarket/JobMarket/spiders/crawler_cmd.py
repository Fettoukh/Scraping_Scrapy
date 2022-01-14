import subprocess
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

working_dir="./"
setting = get_project_settings()
process = CrawlerProcess(setting)
for spider_name in process.spiders.list():
    subprocess.run(["powershell", "-Command", "scrapy crawl "+spider_name+" -o ../data/"+spider_name+".json"])

