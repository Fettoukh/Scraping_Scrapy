import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl marocadres -o ../data/marocadres.json"

class JobOffers_spiders(scrapy.Spider):
    name = "marocadres"
    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'https://www.marocadres.com/liste_offre'
    ]
    # Step 1
    # Step 1
    def parse(self, response):

           # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        response.xpath("//tbody/tr/td[3]//h4/a/@href").extract()
        for offer in response.xpath("//tbody/tr/td[3]//h4/a/@href").extract():
            goto_page = response.urljoin(offer)
            # calls(the second parser after affecting the response to the page containing the details--------
            yield scrapy.Request(goto_page, callback=self.parse_offerpage)
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//a[@class='paginate_button next']/@href").extract()

        if next_page:
            next_page_link = response.urljoin(next_page)
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
        offer_content= w3lib.html.remove_tags(''.join(response.css("table").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r','')).replace("              ","").split("         ")
        desc_poste = w3lib.html.remove_tags(''.join(response.css("table").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r','')).replace("              ","")
        desc_profile = w3lib.html.remove_tags(''.join(response.css(".contentdesc").extract()))
        desc_profile=desc_profile.split('Si vous êtes déjà inscrit comme candidat')[0]
        Secteur=""
        region=""
        metier=""
        date=""
        for information in offer_content:
            if ("Secteur" in information):
                print(information+"----------------------------------------------------------------------------------")

                Secteur = information.split(":")[1]
                print(Secteur+"----------------------------------------------------------------------------------")
            if ("Région" in information):
                region = information.split(":")[1]
            if ("Fonction" in information):
                metier = information.split(":")[-1]
            if ("Statut" in information):
                date = information.split(":")[-1]
        # -------------------
        items = JobmarketItem()
        items['Entreprise'] = ""
        items['Metier'] = metier
        items['Secteur'] = Secteur
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
