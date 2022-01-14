import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl emploi -o ../data/emploi.json"

class JobOffers_spiders(scrapy.Spider):
    name = "emploi"
    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'https://www.emploi.ma/recherche-jobs-maroc'
    ]
    # Step 1
    # Step 1
    def parse(self, response):
        # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        for offer in response.xpath("//div[@class='row']//div[@class='col-lg-5 col-md-5 col-sm-7 col-xs-12 job-title']/h5/a/@href").extract():
            goto_page = response.urljoin(offer)
            # calls(the second parser after affecting the response to the page containing the details--------
            yield scrapy.Request(goto_page, callback=self.parse_offerpage)
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//a[@title='Aller à la page suivante']/@href").extract()

        if next_page:
            next_page_link = response.urljoin(next_page[0])
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    # Step2
    # this parser extract the data and format the data
    def parse_offerpage(self, response):

        Entreprise=w3lib.html.remove_tags(''.join(response.css(".field-name-field-entreprise-secteur .even").extract()))
        Metier=w3lib.html.remove_tags(''.join(response.css(".field-name-field-offre-metiers .even").extract()))
        Secteur=w3lib.html.remove_tags(''.join(response.css(".field-name-field-entreprise-secteur .even").extract()))
        if w3lib.html.remove_tags(''.join(response.css("tr:nth-child(9) td+ td").extract())):
            Nb_poste = w3lib.html.remove_tags(''.join(response.css("tr:nth-child(9) td+ td").extract()))
        else:
            Nb_poste = "1"
        Date=w3lib.html.remove_tags(''.join(response.css(".job-ad-publication-date").extract()))
        Date=Date[-4:]
        Region=w3lib.html.remove_tags(''.join(response.css(".field-name-field-offre-region .even").extract()))
        desc_poste=w3lib.html.remove_tags(''.join(response.css("p+ ul li , .content p").extract()))
        desc_profile=w3lib.html.remove_tags(''.join(response.css(".job-ad-separator+ div").extract()))
        #-------------------
        items = JobmarketItem()
        items['Entreprise'] = Entreprise
        items['Metier'] = Metier
        items['Secteur'] = Secteur
        items['Nb_poste'] = Nb_poste

        items['Date'] = Date
        items['Region'] = Region
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
