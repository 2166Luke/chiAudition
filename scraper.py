from urllib.request import urlopen
import re

url = "https://www.theatreinchicago.com/auditions/"

html = urlopen(url).read().decode('latin-1')

pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags
title = re.sub(" - Theatre In Chicago", "", title) # Remove " - Theatre in Chicago"


def scrapeTIC():
    baseUrl = "https://www.theatreinchicago.com/auditions/"
    homeHtml = urlopen(baseUrl).read().decode('latin-1')

    pattern = r'<div class="post-content">\s*<div class="post-title">\s*<a href="industrydetail\.php\?AuditionID=(\d+)">\s*(.*?)</a>\s*</div>\s*<div class="theatre-name">\s*(.*?)</div>\s*<div class="post-meta">\s*(.*?)</div>\s*</div>'
    match_results = re.findall(pattern, homeHtml, re.IGNORECASE)
    print(match_results)
    for audition in match_results:
        # Extract audition ID
        auditionId = audition[0]

        # Route to the individual audition page and extract the title
        auditionUrl = baseUrl + "industrydetail.php?AuditionID=" + auditionId 
        auditionHtml = urlopen(auditionUrl).read().decode('latin-1')
        pattern = r'<div class="subtitle">\s*(.*?)\s*</div>'
        match_results = re.search(pattern, auditionHtml, re.IGNORECASE)
        if match_results:
            auditionTitle = match_results.group(1)
            print(f"Audition Title: {auditionTitle}")

        # Extract the company
        pattern = r'<div class=\"post-title\">\s*(.*?)\s*</div>'
        match_results = re.search(pattern, auditionHtml, re.IGNORECASE)
        if match_results:
            company = match_results.group(1)
            company = re.sub("<.*?>", "", company) # Remove HTML tags
        
        # Extract the date and time
        pattern = r'<div class'

def pushAudition(title, company, date, time, otherDates, location, description, pay, eqStatus, personnel, source):
    
    print(f"Title: {title}")


scrapeTIC()