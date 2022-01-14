# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobmarketItem(scrapy.Item):
    # define the fields for your item here like:
    Entreprise = scrapy.Field()
    Metier = scrapy.Field()
    Secteur = scrapy.Field()
    Nb_poste = scrapy.Field()
    Date = scrapy.Field()
    Region = scrapy.Field()
    desc_poste=scrapy.Field()
    desc_profile=scrapy.Field()
    #Type_contrat = scrapy.Field()
    #Niveau_formation = scrapy.Field()
   # Niveau_experience = scrapy.Field()
    pass
