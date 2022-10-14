import scrapy


class FemHeadSpider(scrapy.Spider):
    name = 'fem_head'
    allowed_domains = ['en.wikipedia.org/wiki/List_of_elected_and_appointed_female_heads_of_state_and_government']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_elected_and_appointed_female_heads_of_state_and_government']

    # Remove the slash at the end of the path in start_urls if it is still present. 
    # The "/" creates an error when scrapy tries to crawl the data

    def parse(self, response):
        """
        This function aims to extract the name, country, mandate start and mandate end date of each female head of state in the table on the 
        wikipedia page.

        We first identify the tbody of the table and store it in a variable tab. We then exytract the rows of this table in the tr.
        We exclude the first row as it doesnt contain any actual data.
        Then we index over all the rows and for each row we extract the child td.
    
        The wikipedia data of our interest needs to be retrieved from 2 different children ("a" and "span") of this td child.

        We store the text contents of "a" in a variable nam_count as these are the names of the head of the state and the country
        We store the text content of "span" in a variable start_end as these are the mandate start and end dates

        The wikipedia data is not consistent across all rows. The length of the a and span items and the position of their elements 
        varies with each row. 
        Eg. in some rows the start date is the first element of the span item and in some rows it is the second.
        We noticed that the position of the relevant text varies with the length of the item and so we use this with if conditions
        to fix the errors

        Similarly for leaders with mutliple terms, the name and country is provided for the first term but it is missing in the successive 
        terms. 
        If the name and country are not missing then these variables are populated accordingly. If they are missing then the value from
        the previous row is used. 
        They are only missing if they are a successive term, of a head with multiple terms, so using the previous value is valid

        For head of states which are currently in power, we fix the end data as 31 Jan 2022. This is a date larger than all start dates
        in our sample. This is just done to make analysis easier by giving date values to all entries. It doesn't affect our analysis
        otherwise as we will be focusing on 2020 only

        The if conditions take care of all these cleaning errors.

        In the end we store our data in a dictionary named data and we then yield it
        """
        tab= response.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody')
        rows= tab.xpath('.//tr')[1:]
        for row in rows:
            td= row.css("td")
            nam_count= td.css("a::text").getall() #This contains the name of the state and its female head 
            start_end= td.css("span::text").getall() #Start and End Dates of the head's position in power

            #Cleaning
            
            #Extracting Name and Country
            if len(nam_count)>=2:
                name= nam_count[0]    
                country= nam_count[1] 
            
            #Extracting date entries based on each case
            if len(start_end)==5:
                start= start_end[1]
                end= start_end[2]
            if len(start_end)==4:
                start= start_end[2]
                end= start_end[3]
            if len(start_end)==3:
                start= start_end[1]
                end= start_end[2]
            if len(start_end)==2:
                if len(start_end[0])>=4:
                   start= start_end[0]
                   end= start_end[1]
                else:
                   start= start_end[1]
                   end= "31-Jan-22"       #31 Jan 22 entry as end date for heads currently in power
            if len(start_end)==1:
                start= start_end[0]
                end= "31-Jan-22"
            
            
            data={
                "Name": name, 
                "Country":country, 
                "Start_Date":start,
                "End_Date":end
                }
            yield data
