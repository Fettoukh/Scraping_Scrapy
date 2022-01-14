import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl anapec -o ../data/anapec.json"

class JobOffers_spiders(scrapy.Spider):
    name = "anapec"
    items = JobmarketItem()


    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'http://anapec.org/sigec-app-rv/chercheurs/resultat_recherche/page:1/tout:all/language:fr'
    ]
    # Step 1
    # Step 1
    def parse(self, response):

        # myTable > tbody > tr:nth-child(1) > td:nth-child(3)
        # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        for offer in response.css("#myTable > tbody > tr"):
            date=offer.css("td:nth-child(3)::text").extract_first()
            region=offer.css("td:nth-child(6)::text").extract_first()
            metier=offer.css("td:nth-child(4)::text").extract_first()
            link=offer.css("td:nth-child(2) a::attr(href)").extract_first()
            goto_page = response.urljoin(link)
            # calls(the second parser after affecting the response to the page containing the details--------
            yield scrapy.Request(goto_page, callback=self.parse_offerpage, cb_kwargs={'date': date,'region':region,'metier':metier})
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//span[@id='suivant']/parent::a/@href").extract_first()

        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    # Step2
    # this parser extract the data and format the data
    def parse_offerpage(self, response,date,region,metier):

        desc_poste=w3lib.html.remove_tags(''.join(response.css(".info_offre").extract()))
        desc_profile=w3lib.html.remove_tags(''.join(response.css("#oneofmine p , #oneofmine span").extract()))
        items = JobmarketItem()
        items['Entreprise'] = ""
        items['Metier'] = metier
        items['Secteur'] = ""
        items['Nb_poste'] = "1"
        items['Date'] = date
        items['Region'] = region
        items['desc_poste'] = desc_poste
        items['desc_profile'] = desc_profile
        yield items
        # yield {
        #
        #     'Entreprise': Entreprise.encode('utf-8', errors='ignore').decode(),
        #     'Metier':Metier,
        #     'Secteur':Secteur,
        #     'Nombre de poste': Nb_poste,
        #     'Date': Date,
        #     'Region':Region
        #
        #
        # }
