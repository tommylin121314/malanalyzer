from bs4 import BeautifulSoup
import requests as r

class MALExtractor:
    
    def getTopAnimesUpToPage(self, pageNum):
        """
        Gets a dictionary of anime information from the MyAnimeList top animes leaderboard up to a given rank.
        Parameter:
            pageNum: the number of pages from the top animes list to query
        Return:
            Returns a dictionary containing information on the top n animes on the MyAnimeList top animes leaderboard
            Included fields: "name", "link", "
        """

        # Starting URL template for MyAnimeList's top animes leaderboard
        url = "https://myanimelist.net/topanime.php?limit="
        animeData = []

        # Iterates through pages containing 50 animes at a time
        for i in range(pageNum):
            rankingEntries = self.getPageAnimeEntries(url + str(i * 50))
            for entry in rankingEntries:
                animeURL = self.getAnimeURL(entry)
                animeData.append(self.getDataFromAnimeURL(animeURL))
        return animeData
    

    def getAnimeURL(self, rankingEntry):
        entryH3 = rankingEntry.find("h3", "anime_ranking_h3")
        return entryH3.find("a")["href"]

    def getPageAnimeEntries(self, pageURL):
        pageSoup = BeautifulSoup(r.get(pageURL).text, "html.parser")
        rankingTable = pageSoup.find("table", "top-ranking-table")
        return rankingTable.find_all("tr", "ranking-list")

    def getDataFromAnimeURL(self, animeURL):
        print(animeURL)
        entrySoup = BeautifulSoup(r.get(animeURL).text, "html.parser")
        return {
            "Name": self.getAnimeName(entrySoup),
            "Type": self.getAnimeType(entrySoup),
            "Score": self.getAnimeScore(entrySoup),
            "Begin": self.getAnimeBegin(entrySoup),
            "End": self.getAnimeEnd(entrySoup),
            "Episodes": self.getAnimeEpisodes(entrySoup),
            "Studios": self.getAnimeStudios(entrySoup),
            "Demographic": self.getAnimeDemographic(entrySoup),
            "Season": self.getAnimeSeason(entrySoup),
            "Genres": self.getAnimeGenres(entrySoup),
            "Themes": self.getAnimeThemes(entrySoup),
            "RatingCount": self.getAnimeRatingCount(entrySoup),
            "Members": self.getAnimeMembers(entrySoup),
            "Favorites": self.getAnimeFavorites(entrySoup),
            "Popularity": self.getAnimePopularity(entrySoup),
            "Link": animeURL,
        }
    
    def getAnimeName(self, entrySoup):
        if entrySoup.find("h1", "title-name"):
           return entrySoup.find("h1", "title-name").text
    
    def getAnimeType(self, entrySoup):
        if entrySoup.find("span", string="Type:"):
           return entrySoup.find("span", string="Type:").next_sibling.next_sibling.text
        
    def getAnimeBegin(self, entrySoup):
        if entrySoup.find("span", string="Aired:"):
            entryAired = entrySoup.find("span", string="Aired:").next_sibling.text.split("to")
            return entryAired[0].strip()
    
    def getAnimeEnd(self, entrySoup):
        if entrySoup.find("span", string="Aired:"):
            entryAired = entrySoup.find("span", string="Aired:").next_sibling.text.split("to")
            if len(entryAired) > 1:
                return entryAired[1].strip()
            else:
                return "n/a"
        
    def getAnimeEpisodes(self, entrySoup):
        if entrySoup.find("span", string="Episodes:"):
            return entrySoup.find("span", string="Episodes:").next_sibling.text.strip()
        
    def getAnimeStudios(self, entrySoup):
        if entrySoup.find("span", string="Studios:"):
            return entrySoup.find("span", string="Studios:").next_sibling.next_sibling.text
        
    def getAnimeDemographic(self, entrySoup):
        if entrySoup.find("span", string="Demographic:"):
            return entrySoup.find("span", string="Demographic:").next_sibling.next_sibling.text
        
    def getAnimeSeason(self, entrySoup):
        if entrySoup.find("span", string="Premiered:"):
            return entrySoup.find("span", string="Premiered:").next_sibling.next_sibling.text

    def getAnimeGenres(self, entrySoup): 
        if entrySoup.find("span", string="Genres:"):
            return [genre_item.text for genre_item in entrySoup.find("span", string="Genres:").find_next_siblings("a")]
        elif entrySoup.find("span", string="Genre:"):
            return [genre_item.text for genre_item in entrySoup.find("span", string="Genre:").find_next_siblings("a")]
        
    def getAnimeThemes(self, entrySoup):
        if entrySoup.find("span", string="Themes:"):
            return [theme_item.text for theme_item in entrySoup.find("span", string="Themes:").find_next_siblings("a")]
        elif entrySoup.find("span", string="Theme:"):
            return [theme_item.text for theme_item in entrySoup.find("span", string="Theme:").find_next_siblings("a")]
        
    def getAnimeScore(self, entrySoup):
        if entrySoup.find("span", {"itemprop": "ratingValue"}):
            return entrySoup.find("span", {"itemprop": "ratingValue"}).text
        
    def getAnimeRatingCount(self, entrySoup):
        if entrySoup.find("span", {"itemprop": "ratingCount"}):
            return entrySoup.find("span", {"itemprop": "ratingCount"}).text
        
    def getAnimePopularity(self, entrySoup):
        if entrySoup.find("span", string="Popularity:"):
            return entrySoup.find("span", string="Popularity:").next_sibling.text.strip().replace("#", "")
        
    def getAnimeFavorites(self, entrySoup):
        if entrySoup.find("span", string="Favorites:"):
            return entrySoup.find("span", string="Favorites:").next_sibling.text.strip() 
        
    def getAnimeMembers(self, entrySoup):
        if entrySoup.find("span", string="Members:"):
            return entrySoup.find("span", string="Members:").next_sibling.text.strip() 