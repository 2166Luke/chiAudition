from urllib.request import urlopen
import re

def scrapeTIC():
    baseUrl = "https://www.theatreinchicago.com/auditions/"
    homeHtml = urlopen(baseUrl).read().decode('latin-1')

    pattern = r'<div class=\"post-content\">\s*<div>(.*?)</div>\s*<div class=\"post-title\">\s*<a href=\"industrydetail.php\?AuditionID=(\d+)\">\s*<strong>(.*?)</strong>\s*</a>\s*</div>\s*<div class=\"theatre-name\">\s*(.*?)\s*</div>\s*<div class=\"post-meta\">\s*<b>.*</b>(?:\s*(.*?)\s*<br><br>)?\s*</div>'
    match_results = re.findall(pattern, homeHtml, re.IGNORECASE)
    for audition in match_results:
        # Create variables from data on the auditions landing page
        company = audition[0]
        auditionId = audition[1]
        title = audition[2]
        status = audition[3]
        if audition[4] != '':
            dates = audition[4]
        else:
            dates = "N/A"
        print(company, "    ", title, "    ", status, "    ", dates)

        # Route to the individual audition page and extract the title
        auditionUrl = baseUrl + "industrydetail.php?AuditionID=" + auditionId 
        auditionHtml = urlopen(auditionUrl).read().decode('latin-1')
        
        

def pushAudition(title, company, date, time, otherDates, location, description, pay, eqStatus, personnel, source):
    
    print(f"Title: {title}")


scrapeTIC()