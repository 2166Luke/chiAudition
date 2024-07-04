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

        # Route to the individual audition page and extract the title
        auditionUrl = baseUrl + "industrydetail.php?AuditionID=" + auditionId
        source = "<a href="+auditionUrl+">Theatre In Chicago</a>"
        location = "Chicagoland"

        # Extract pay status from audition site
        auditionHtml = urlopen(auditionUrl).read().decode('latin-1')
        pattern = r'<div class=\"auditions-meta\">\s*<p>\s*.*\s*(.*?)\s*</p>'
        payStatus = re.search(pattern, auditionHtml, re.IGNORECASE).group(1)

        # Extract description from audition site
        start_index = auditionHtml.find("div class=\"post-description\">") + len("div class=\"post-description\">")
        end_index = auditionHtml.find("<div id=\"contact\"")
        description = auditionHtml[start_index:end_index]
        CLEANR = re.compile('<.*?>')
        clean_description = re.sub(CLEANR, '', description)

        personnel = "Check Description"
        print(source)

        pushAudition(title, company, dates, location, clean_description, payStatus, status, personnel, source)

def pushAudition(title, company, dates, location, description, pay, eqStatus, personnel, source):
    
    print(f"Title: {title}")


scrapeTIC()