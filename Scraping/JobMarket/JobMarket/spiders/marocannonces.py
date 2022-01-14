import scrapy
from ..items import JobmarketItem
import w3lib.html
import logging
#the command to run "scrapy crawl marocannonces -o ../data/marocannonces.json"
# scrapy list|xargs -n 1 echo spider
class JobOffers_spiders(scrapy.Spider):
    name = "marocannonces"
    #----------prepare the url starter urls that we re going to scrap from-----------
    start_urls = [
        'https://www.marocannonces.com/categorie/309/Emploi/Offres-emploi.html'
    ]
    # Step 1
    # Step 1
    def parse(self, response):
        # --------get the html tree of the page && look for specific elements in the tree --tags & attributes ---------
        # for offer in response.xpath("//div[@class='content_box']/ul[@class='cars-list']/li/div[@class='block_img']/a/@href").extract():
        for offer in response.css(".cars-list li"):
            # offer_cont=w3lib.html.remove_tags(offer.xpath("/div[@class='holder']/h3/a/@href").extract_first())
            link=offer.css("h3  a::attr(href)").extract_first()
            date=w3lib.html.remove_tags(''.join(offer.css(".date").extract()))
            title=w3lib.html.remove_tags(''.join(offer.css(".holder a").extract()))


            print("---------------------------------------------------------------------------------------------------")
            print(link)
            print(date)
            print("---------------------------------------------------------------------------------------------------")
            goto_page= response.urljoin(link)

            # calls(the second parser after affecting the response to the page containing the details--------

            yield scrapy.Request(goto_page, callback=self.parse_offerpage,cb_kwargs={'title':title})
            # --------look for element that allow to proceed to the next page in the tree --tags & attributes ---------
        next_page = response.xpath("//div[@class='contentpaging']/ul[@class='paging']/li[@class='pagina_suivant']/a/@href").extract_first()

        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    # Step2
    # this parser extract the data and format the data
    def parse_offerpage(self, response,title):

        offreInformation = w3lib.html.remove_tags(''.join(response.css("#extraQuestionName").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        offreInformationList = offreInformation.split("            ")
        Secteur = ""
        Metier = ""
        Entreprise = ""
        Region=w3lib.html.remove_tags(''.join(response.css(".info-holder a").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        desc_poste=w3lib.html.remove_tags(''.join(response.css("#content p").extract()).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ').replace('\r',''))
        # Date = w3lib.html.remove_tags(
        #     ''.join(response.css(".info-holder li:nth-child(2)").extract()).replace('\t', '').replace('\n', '').replace(
        #         u'\xa0', ' ').replace('\r', ''))
        Date=title
        for information in offreInformationList:
            if("Domaine" in information):
                Secteur = information.split(":")[1]
            if ("Fonction" in information):
                Metier = information.split(":")[1]
                if(Metier is ""):
                    Metier=''.join(response.css("h1").extract())
            if ("Entreprise" in information):
                Entreprise = information.split(":")[1]
            # if Date.find("Publiée le") is -1:
            #     Date=link
        #-------------------
        items = JobmarketItem()
        items['Entreprise'] = Entreprise
        items['Metier'] = Metier
        items['Secteur'] = Secteur
        items['Nb_poste'] = "1"
        items['Date'] = Date
        items['Region'] = Region
        items['desc_poste'] =desc_poste
        items['desc_profile'] = ""
        yield items


