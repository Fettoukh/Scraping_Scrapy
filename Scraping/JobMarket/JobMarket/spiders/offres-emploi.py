import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl offre-emploi -o ../data/offre-emploi.json"

class JobOffers_spiders(scrapy.Spider):
    name = "offre-emploi"
    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'https://www.offres-emploi.ma/emploi-public.mc'
    ]
    # Step 1
    # Step 1
    def parse(self, response):
        # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        for offer in response.xpath("//div[@class='offre-content']/h2/a/@href").extract():
            goto_page = response.urljoin(offer)
            # calls(the second parser after affecting the response to the page containing the details--------
            yield scrapy.Request(goto_page, callback=self.parse_offerpage)
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//a[@title='Emploi emploi-public >']/@href").extract()

        if next_page:
            next_page_link=''.join(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    # Step2
    # this parser extract the data and format the data
    def parse_offerpage(self, response):

        # Entreprise=w3lib.html.remove_tags(''.join(response.css(".table-sm:nth-child(1) tr:nth-child(1) td , tr:nth-child(9) td").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Metier=w3lib.html.remove_tags(''.join(response.css("tr:nth-child(2) td").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Secteur=w3lib.html.remove_tags(''.join(response.css(".field-name-field-entreprise-secteur .even").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Nb_poste=w3lib.html.remove_tags(''.join(response.css("tr:nth-child(4) td").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Date=w3lib.html.remove_tags(''.join(response.css("tr:nth-child(5) td").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Date=Date[-4:]
        # Region=w3lib.html.remove_tags(''.join(response.css(".field-name-field-offre-region .even").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        offer_content=w3lib.html.remove_tags(''.join(response.css(".offre-content-detail").extract()).replace('\t', '').replace(u'\xa0', ' ')).split(("\r\n                  \r\n                  \r\n "))
        desc_poste=w3lib.html.remove_tags(''.join(response.css(".offre-content-detail").extract()).replace('\t', '').replace(u'\xa0', ' '))
        desc_profile=w3lib.html.remove_tags(''.join(response.css(".ads9849892952+ p").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        date=w3lib.html.remove_tags(''.join(response.css(".date").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        secteur=w3lib.html.remove_tags(''.join(response.css(".company a").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        #-------------------
        region = "nationale"
        metier = ""
        nb_poste="1"
        entreprise=""
        for information in offer_content:
            if ("organisatrice" in information):
                entreprise = information.split(":")[-1]
            if ("Nombre de postes" in information):
                nb_poste = information.split(":")[1]
            if ("Poste" in information):
                metier = information.split(":")[-1]

        items = JobmarketItem()
        items['Entreprise'] = entreprise.replace('\r', '').replace('\n', '').replace('  ', '')
        items['Metier'] =metier.replace('\r', '').replace('\n', '').replace('  ', '')
        items['Secteur'] =secteur.replace('\r', '').replace('\n', '').replace('  ', '')
        items['Nb_poste'] = nb_poste.replace('\r', '').replace('\n', '').replace('  ', '')
        items['Date'] = date.replace('\r', '').replace('\n', '').replace('  ', '')
        items['Region'] = region
        items['desc_poste'] = desc_poste.replace('\r', '').replace('\n', '').replace('  ', '')
        items['desc_profile'] = desc_profile.replace('\r', '').replace('\n', '').replace('  ', '')

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
