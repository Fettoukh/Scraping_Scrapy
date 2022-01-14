import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl rekrute -o ../data/rekrute.json"

class JobOffers_spiders(scrapy.Spider):
    name = "rekrute"
    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'https://www.rekrute.com/offres.html'
    ]
    # Step 1
    def parse(self, response):
        # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        for offer in response.xpath("//li[@class='post-id']//div[@class='section']/h2/a/@href").extract():
            goto_page = response.urljoin("./" + offer)

            #calls(the second parser after affecting the response to the page containing the details--------
            yield scrapy.Request(goto_page, callback=self.parse_offerpage)
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page  is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    # Step2
    #this parser extract the data and format the data
    def parse_offerpage(self, response):

        Entreprise=''.join(response.xpath("//div[@id='recruiterDescription']/p/text()").extract_first())
        Metier=''.join(response.xpath("//div[@class='col-md-4']/span/text()").extract_first())
        Metier=Metier[4:].replace(' ','')
        Secteur=''.join(response.xpath("//div[@class='col-md-5']/strong/following-sibling::text()").extract_first())
        Secteur=Secteur[4:]
        if response.xpath("//div[@class='col-md-3']/span/text()").extract_first() :
            Nb_poste=''.join(response.xpath("//div[@class='col-md-3']/span/text()").extract_first())
        else :
            Nb_poste="1"
        Date=''.join(response.xpath("//div[@class='col-md-5']/strong[3]/following-sibling::text()").extract_first())
        Date=Date[-4:]
        Region=''.join(response.xpath("//div[@class='col-md-5']/strong[2]/following-sibling::text()").extract_first())
        Region=Region[4:]


        desc_poste=w3lib.html.remove_tags(''.join(response.css("info").extract()))
        desc_poste=desc_poste[4:]
        desc_profile=w3lib.html.remove_tags(''.join(response.css(".blc:nth-child(5) , .blc:nth-child(6)").extract()))
        desc_profile=desc_profile[4:]
        #-------------------
        items = JobmarketItem()
        items['Entreprise']=Entreprise
        items['Metier'] = Metier
        items['Secteur'] = Secteur
        items['Nb_poste'] = Nb_poste
        items['Date'] = Date
        items['Region'] = Region
        items['desc_poste']=desc_poste
        items['desc_profile']=desc_profile
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
