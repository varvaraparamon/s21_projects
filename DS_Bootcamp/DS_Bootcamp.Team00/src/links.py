import requests
from bs4 import BeautifulSoup
from collections import Counter

class Links:
    """
    Analyzing data from links.csv
    """
    @staticmethod
    def parse_csv_line(line):
        return [x.strip() for x in line.strip().split(',')]

    @staticmethod
    def top_n(dict_inp, n):
        sorted_dict_inp =  dict(sorted(dict_inp.items(), key = lambda x: x[1], reverse = True))    
        return dict(list(sorted_dict_inp.items())[:n])

    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.links_dict = {"movieId":[], "imdbId":[], "tmdbId":[]}
        with open(self.path, "r") as file:
            headers = file.readline()
            for i in range(10):
                try:
                    parsed_line = self.parse_csv_line(file.readline())
                    self.links_dict["movieId"].append(int(parsed_line[0]) if parsed_line[0] != "" else None)
                    self.links_dict["imdbId"].append(parsed_line[1] if parsed_line[1] != "" else None)
                    self.links_dict["tmdbId"].append(int(parsed_line[2]) if parsed_line[2] != "" else None)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line {i+2}\n", e)
        self.imdb_info = self.get_imdb(self.links_dict["movieId"], ["Director", "Budget", "Cumulative Worldwide Gross", "Runtime", "Title"])
    
    def get_imdb(self, list_of_movies, list_of_fields):
        """
The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
     Sort it by movieId descendingly.
        """
        imdb_info = []
        for movie_id in sorted(list_of_movies, reverse=True):
            movie_info = [movie_id]
            try: 
                i_imdb = self.links_dict["movieId"].index(movie_id)
                imdb_id = self.links_dict["imdbId"][i_imdb]

                headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                link = f"https://www.imdb.com/title/tt{imdb_id}/"
                response = requests.get(link, headers=headers)
                response.raise_for_status() 
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for field in list_of_fields:
                    res = None
                    if field == "Budget":
                        field_tag = soup.find(string=field)
                        res = field_tag.find_next().text.strip() if field_tag else None
                        res = "".join(res[1:].split()[0].split(",")) if field_tag else None
                    elif field == "Cumulative Worldwide Gross":
                        field = "Gross worldwide"
                        field_tag = soup.find(string=field)
                        res = field_tag.find_next().text.strip() if field_tag else None
                        res = "".join(res[1:].split()[0].split(",")) if field_tag else None
                    elif field == "Runtime":
                        field_tag = soup.find(string=field) 
                        res = field_tag.find_next().text.strip().split() if field_tag else None
                        res = int(res[0])*60 + int(res[2]) if res[2] else int(res[0]) if field_tag else None
                    elif field == "Title":
                        field_tag = soup.find(class_="hero__primary-text")
                        res = field_tag.text.strip() if field_tag else None
                    else:
                        field_tag = soup.find(string=field)
                        res = field_tag.find_next().text.strip() if field_tag else None
                    movie_info.append(res)


            
            except (ValueError, IndexError, requests.exceptions.RequestException) as e:
                print(f"Error processing movieId {movie_id}: {e}")
            imdb_info.append(movie_info)
        
        return imdb_info
        
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        # imdb_list = self.get_imdb(self.links_dict["movieId"], ["Director"])
        directors_list = [item[1] for item in self.imdb_info if item[1] != None]
        directors_dict = Counter(directors_list)

        directors = directors_dict.most_common(n)
        return directors
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        budgets = {mov[-1] : mov[2] 
                   for mov in self.imdb_info 
                   if mov[2] != None}
        
        return self.top_n(budgets, n)
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
        profits = {mov[-1] : int(mov[3])-int(mov[2]) 
                   for mov in self.imdb_info 
                   if (mov[2] != None) and (mov[3] != None)}

        return self.top_n(profits, n)
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
     Sort it by runtime descendingly.
        """
        runtimes = {mov[-1] : mov[4] 
                    for mov in self.imdb_info
                    if mov[4] != None}

        return self.top_n(runtimes, n)
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        costs = {mov[-1] : round(float(mov[2])/float(mov[4]), 2)
                   for mov in self.imdb_info 
                   if (mov[2] != None) and (mov[4] != None)}
        
        return self.top_n(costs, n)

l = Links("ml-latest-small/links.csv")
# print(l.get_imdb([1, 2, 3, 4, 5, 6, 7, 8, 9], ["Director", "Budget", "Cumulative Worldwide Gross", "Runtime"]))
print(l.top_directors(2))
print(l.most_expensive(3))
print(l.most_profitable(3))
print(l.longest(3))
print(l.top_cost_per_minute(3))



