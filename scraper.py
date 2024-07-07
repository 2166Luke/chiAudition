from urllib.request import urlopen
from cs50 import SQL
import datetime
import calendar
import re

def scrapeTIC():
    month_dict = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    baseUrl = "https://www.theatreinchicago.com/auditions/"
    homeHtml = urlopen(baseUrl).read().decode('latin-1')

    pattern = r'<div class=\"post-content\">\s*<div>(.*?)</div>\s*<div class=\"post-title\">\s*<a href=\"industrydetail.php\?AuditionID=(\d+)\">\s*<strong>(.*?)</strong>\s*</a>\s*</div>\s*<div class=\"theatre-name\">\s*(.*?)\s*</div>\s*<div class=\"post-meta\">\s*<b>.*</b>(?:\s*(.*?)\s*<br><br>)?\s*</div>'
    match_results = re.findall(pattern, homeHtml, re.IGNORECASE)
    for audition in match_results:
        # Create variables from data on the auditions landing page
        company = audition[0]
        auditionId = audition[1]
        title = audition[2]
        eqStatus = audition[3]
        if audition[4] != '':
            dates = audition[4]
        else:
            dates = "Check Description"        
        firstDate = "N/A"
        lastDate = "N/A"

        # Translate extracted date values into datetime format and set first and last dates for sorting
        if dates != "Check Description":
            year = datetime.datetime.now().year
            if len(dates) < 8:
                pattern = r'(.*?) (\d+)'
                match_results = re.findall(pattern, dates, re.IGNORECASE)
                month = match_results[0][0]
                month = month_dict[month]
                day = match_results[0][1]
                firstDate = datetime.date(int(year), month, int(day))
                lastDate = firstDate
            else:
                pattern = r'(.*?) (\d+) - (.*?) (\d+)'
                match_results = re.findall(pattern, dates, re.IGNORECASE)
                month1 = match_results[0][0]
                month1 = month_dict[month1]
                day1 = match_results[0][1]
                firstDate = datetime.date(int(year), int(month1), int(day1))
                month2 = match_results[0][2]
                month2 = month_dict[month2]
                day2 = match_results[0][3]
                lastDate = datetime.date(int(year), int(month2), int(day2))

        # Route to the individual audition page and extract the title
        auditionUrl = baseUrl + "industrydetail.php?AuditionID=" + auditionId
        source = "<a href="+auditionUrl+">Theatre In Chicago</a>"
        location = "Chicagoland"
        upcoming = 1

        # Extract pay status from audition site
        auditionHtml = urlopen(auditionUrl).read().decode('latin-1')
        pattern = r'<div class=\"auditions-meta\">\s*<p>\s*.*\s*(.*?)\s*</p>'
        payStatus = re.search(pattern, auditionHtml, re.IGNORECASE).group(1)

        # Extract the post date from listings without scrapable audition dates set last day to 2 weeks later
        if dates == "Check Description":
            pattern = r'<p class=\"text-center\">Posted Date: (.*)</p>'
            match_results = re.search(pattern, auditionHtml, re.IGNORECASE).group(1)
            pattern = r'(.*?) (\d+), (\d+)'
            match_results = re.findall(pattern, match_results, re.IGNORECASE)
            month = match_results[0][0]
            month = month_dict[month]
            day = match_results[0][1]
            year = match_results[0][2]
            post_date = datetime.date(int(year), month, int(day))
            lastDate = post_date + datetime.timedelta(weeks=4)

        # Extract description from audition site
        start_index = auditionHtml.find("div class=\"post-description\">") + len("div class=\"post-description\">")
        end_index = auditionHtml.find("<div id=\"contact\"")
        description = auditionHtml[start_index:end_index]
        CLEANR = re.compile('<.*?>')
        clean_description = re.sub(CLEANR, '', description)

        personnel = "Check Description"
        
        pushAudition(title, company, dates, location, clean_description, payStatus, eqStatus, personnel, source, firstDate, lastDate, upcoming)

def scrapeLOCT():
    # TBD: Implement scraping logic for LOCT
    location = Chicagoland
    baseUrl = "https://auditions.leagueofchicagotheatres.org/"

def pushAudition(title, company, dates, location, description, pay, eqStatus, personnel, source, firstDate, lastDate, upcoming):
    #search database for existing posting
    db = SQL("sqlite:///auditions.db")
    search = db.execute("SELECT * FROM auditions WHERE source = (?)", [source])
    if search:
        print("Audition already in database")
        return
    else:
        db.execute("INSERT INTO auditions (title, company, dates, location, description, pay, eqStatus, personnel, source, firstDate, lastDate, upcoming) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", title, company, dates, location, description, pay, eqStatus, personnel, source, firstDate, lastDate, upcoming)

        #print success message
        print("Audition pushed to database successfully")

scrapeTIC()