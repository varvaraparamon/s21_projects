import re
from collections import defaultdict, OrderedDict, Counter
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Movies:
    @staticmethod
    def parse_csv_line(line):
        pattern = re.compile(r'(?:^|,)(?:"([^"]*)"|([^",]*))')
        values = []
        for match in pattern.finditer(line.strip()):
            value = match.group(1) if match.group(1) is not None else match.group(2)
            values.append(value.strip())
        return values

    def __init__(self, file_path):
        self.data = defaultdict(list)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            header_line = next(file)
            headers = self.parse_csv_line(header_line)
            
            for i, line in enumerate(file, 1):
                if i > 1000:
                    break
                if line.strip():
                    values = self.parse_csv_line(line)
                    for header, value in zip(headers, values):
                        if header == 'movieId':
                            value = int(value)
                        self.data[header].append(value)

    def dist_by_release(self):
        year_counts = defaultdict(int)
        
        for title in self.data['title']:
            match = re.search(r'\((\d{4})\)$', title)
            if match:
                year = int(match.group(1))
                year_counts[year] += 1
        
        return OrderedDict(sorted(year_counts.items(), 
                              key=lambda x: x[1], 
                              reverse=True))

    def dist_by_genres(self):
        genre_counts = defaultdict(int)
        
        for genres_str in self.data['genres']:
            genres = [g.strip() for g in genres_str.split('|') if g.strip()]
            for genre in genres:
                genre_counts[genre] += 1
        
        return OrderedDict(sorted(genre_counts.items(), 
                               key=lambda x: x[1], 
                               reverse=True))

    def most_genres(self, n):
        movies_with_genre_counts = {}
    
        for title, genres_str in zip(self.data['title'], self.data['genres']):
            genres = [g for g in genres_str.split('|') if g]
            movies_with_genre_counts[title] = len(genres)
    
        sorted_movies = OrderedDict(
            sorted(movies_with_genre_counts.items(), 
                key=lambda item: item[1], 
                reverse=True)[:n]
        )   
    
        return sorted_movies



class Ratings:

    @staticmethod
    def parse_csv_line(line):
        return [x.strip() for x in line.strip().split(',')]

    def __init__(self, path_to_the_file):
        self.data = defaultdict(list)
        
        with open(path_to_the_file, 'r', encoding='utf-8') as file:
            headers = self.parse_csv_line(next(file))
            
            for i, line in enumerate(file, 1):
                if i > 1000:
                    break
                if line.strip():
                    values = self.parse_csv_line(line)
                    try:
                        self.data['userId'].append(int(values[0]))
                        self.data['movieId'].append(int(values[1]))
                        self.data['rating'].append(float(values[2]))
                        self.data['timestamp'].append(int(values[3]))
                    except (ValueError, IndexError) as e:
                        raise ValueError(f"Error parsing line {i}: {line}") from e
                    
    class Movies:

        @staticmethod
        def parse_csv_line(line):
            return [x.strip() for x in line.strip().split(',')]
        
        def __init__(self, ratings_data, movies_path):
            self.enriched_data = defaultdict(list)
            
            movie_info = self._load_movie_info(movies_path)
            
            for i in range(len(ratings_data['movieId'])):
                movie_id = ratings_data['movieId'][i]
                if movie_id in movie_info:
                    for key in ratings_data:
                        self.enriched_data[key].append(ratings_data[key][i])
                    self.enriched_data['title'].append(movie_info[movie_id]['title'])
                    self.enriched_data['genres'].append(movie_info[movie_id]['genres'])

        def _load_movie_info(self, movies_path):
            movie_info = {}
            with open(movies_path, 'r', encoding='utf-8') as file:
                headers = self.parse_csv_line(next(file))
                for line in file:
                    values = self.parse_csv_line(line)
                    if len(values) == len(headers):
                        movie_id = int(values[0])
                        movie_info[movie_id] = {
                            'title': values[1],
                            'genres': values[2].split('|')
                        }
            return movie_info

        def dist_by_year(self):
            year_counts = defaultdict(int)
            for timestamp in self.enriched_data['timestamp']:
                year = datetime.fromtimestamp(timestamp).year
                year_counts[year] += 1
            return OrderedDict(sorted(year_counts.items()))

        def top_by_num_of_ratings(self, n):
            movie_counts = defaultdict(int)
            for title in self.enriched_data['title']:
                movie_counts[title] += 1
            
            return OrderedDict(
                sorted(movie_counts.items(),
                      key=lambda x: x[1],
                      reverse=True)[:n]
            )

        def dist_by_rating(self):
            rating_counts = defaultdict(int)
            for rating in self.enriched_data['rating']:
                rating_counts[rating] += 1
            return OrderedDict(sorted(rating_counts.items()))
        

        def top_by_ratings(self, n, metric):
            movie_ratings = defaultdict(list)
            for movie_id, rating in zip(self.enriched_data['movieId'], self.enriched_data['rating']):
                movie_ratings[movie_id].append(rating)

            movie_stats = {}
            for movie_id, ratings in movie_ratings.items():
                if metric == 'average':
                    value = round(sum(ratings) / len(ratings), 2)
                else:
                    sorted_ratings = sorted(ratings)
                    length = len(sorted_ratings)
                    if length % 2 == 1:
                        value = round(sorted_ratings[length//2], 2)
                    else:
                        value = round((sorted_ratings[length//2 - 1] + sorted_ratings[length//2]) / 2, 2)
                movie_stats[movie_id] = value

            title_to_rating = {}
            for i, movie_id in enumerate(self.enriched_data['movieId']):
                if movie_id in movie_stats:
                    title = self.enriched_data['title'][i]
                    title_to_rating[title] = movie_stats[movie_id]

            sorted_movies = sorted(title_to_rating.items(), key=lambda x: x[1], reverse=True)

            return OrderedDict(sorted_movies[:n])
        
    
        def top_controversial(self, n):
            movie_ratings = defaultdict(list)
            for movie_id, rating in zip(self.enriched_data['movieId'], self.enriched_data['rating']):
                movie_ratings[movie_id].append(rating)
            movie_variances = {}
            for movie_id, ratings in movie_ratings.items():
                if len(ratings) >= 2:
                    mean = sum(ratings) / len(ratings)
                    variance = sum((x - mean) ** 2 for x in ratings)
                    movie_variances[movie_id] = variance / (len(ratings) - 1)
            
            title_to_variance = {}
            for i, movie_id in enumerate(self.enriched_data['movieId']):
                if movie_id in movie_variances:
                    title = self.enriched_data['title'][i]
                    title_to_variance[title] = movie_variances[movie_id]
            
            sorted_movies = sorted(title_to_variance.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
            
            return OrderedDict(sorted_movies[:n])


class Tags:
    @staticmethod
    def parse_csv_line(line):
        pattern = re.compile(r'(?:^|,)(?:"([^"]*)"|([^",]*))')
        values = []
        for match in pattern.finditer(line.strip()):
            value = match.group(1) if match.group(1) is not None else match.group(2)
            values.append(value.strip())
        return values

    def __init__(self, file_path):
        self.data = defaultdict(list)
    
        with open(file_path, 'r', encoding='utf-8') as file:
            header_line = next(file)
            headers = self.parse_csv_line(header_line)
        
            for i, line in enumerate(file, 1):
                if i > 1000:
                    break
                if line.strip():
                    values = self.parse_csv_line(line)
                    for header, value in zip(headers, values):
                        if header in ['userId', 'movieId', 'timestamp']:
                            value = int(value)
                        self.data[header].append(value)

    def most_words(self, n):
        tag_word_counts = {}
        for tag in set(self.data['tag']):
            tag_word_counts[tag] = len(tag.split())
        return OrderedDict(sorted(tag_word_counts.items(), key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        unique_tags = list(set(self.data['tag']))
        unique_tags.sort(key=lambda x: len(x), reverse=True)
        return unique_tags[:n]

    def most_words_and_longest(self, n):
        most_words = set(dict(self.most_words(n)).keys())
        longest = set(self.longest(n))
        return sorted(most_words & longest)

    def most_popular(self, n):
        tag_counts = defaultdict(int)
        for tag in self.data['tag']:
            tag_counts[tag] += 1
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:n])

    def tags_with(self, word):
        matching_tags = sorted(list({tag for tag in self.data['tag'] 
                                  if word.lower() in tag.lower()}))
        return matching_tags


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
            for i in range(5):
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
    




import pytest


MOVIES_PATH = 'ml-latest-small/movies.csv'
RATINGS_PATH = 'ml-latest-small/ratings.csv'
TAGS_PATH = 'ml-latest-small/tags.csv'
LINKS_PATH = 'ml-latest-small/links.csv'

@pytest.fixture
def movies_instance():
    return Movies(MOVIES_PATH)

@pytest.fixture
def ratings_instance():
    return Ratings(RATINGS_PATH)

@pytest.fixture
def tags_instance():
    return Tags(TAGS_PATH)

@pytest.fixture
def links_instance():
    return Links(LINKS_PATH)

class TestMovies:
    def test_init_data_types(self, movies_instance):
        assert isinstance(movies_instance.data, defaultdict)
        for key, value_list in movies_instance.data.items():
            assert isinstance(value_list, list)
            if key == 'movieId':
                assert all(isinstance(x, int) for x in value_list)
            else:
                assert all(isinstance(x, str) for x in value_list)

    def test_dist_by_release(self, movies_instance):
        result = movies_instance.dist_by_release()
        assert isinstance(result, OrderedDict)
        assert all(isinstance(k, int) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_dist_by_genres(self, movies_instance):
        result = movies_instance.dist_by_genres()
        assert isinstance(result, OrderedDict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_most_genres(self, movies_instance):
        n = 5
        result = movies_instance.most_genres(n)
        assert isinstance(result, OrderedDict)
        assert len(result) == n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

class TestRatings:
    def test_init_data_types(self, ratings_instance):
        assert isinstance(ratings_instance.data, defaultdict)
        for key, value_list in ratings_instance.data.items():
            assert isinstance(value_list, list)
            if key in ['userId', 'movieId', 'timestamp']:
                assert all(isinstance(x, int) for x in value_list)
            elif key == 'rating':
                assert all(isinstance(x, float) for x in value_list)

    def test_movies_subclass_init(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        assert isinstance(movies_ratings.enriched_data, defaultdict)
        required_keys = ['userId', 'movieId', 'rating', 'timestamp', 'title', 'genres']
        assert all(key in movies_ratings.enriched_data for key in required_keys)

    def test_dist_by_year(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        result = movies_ratings.dist_by_year()
        assert isinstance(result, OrderedDict)
        assert all(isinstance(k, int) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_top_by_num_of_ratings(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        n = 5
        result = movies_ratings.top_by_num_of_ratings(n)
        assert isinstance(result, OrderedDict)
        assert len(result) == n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_dist_by_rating(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        result = movies_ratings.dist_by_rating()
        assert isinstance(result, OrderedDict)
        assert all(isinstance(k, float) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        keys = list(result.keys())
        assert keys == sorted(keys)

    def test_top_by_ratings(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        n = 5
        for metric in ['average', 'median']:
            result = movies_ratings.top_by_ratings(n, metric)
            assert isinstance(result, OrderedDict)
            assert len(result) <= n  
            assert all(isinstance(k, str) for k in result.keys())
            assert all(isinstance(v, float) for v in result.values())
            values = list(result.values())
            assert values == sorted(values, reverse=True)

    def test_top_controversial(self, ratings_instance):
        movies_ratings = Ratings.Movies(ratings_instance.data, MOVIES_PATH)
        n = 5
        result = movies_ratings.top_controversial(n)
        assert isinstance(result, OrderedDict)
        assert len(result) <= n  
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

class TestTags:
    def test_init_data_types(self, tags_instance):
        assert isinstance(tags_instance.data, defaultdict)
        for key, value_list in tags_instance.data.items():
            assert isinstance(value_list, list)
            if key in ['userId', 'movieId', 'timestamp']:
                assert all(isinstance(x, int) for x in value_list)
            else:
                assert all(isinstance(x, str) for x in value_list)

    def test_most_words(self, tags_instance):
        n = 5
        result = tags_instance.most_words(n)
        assert isinstance(result, OrderedDict)
        assert len(result) == n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_longest(self, tags_instance):
        n = 5
        result = tags_instance.longest(n)
        assert isinstance(result, list)
        assert len(result) == n
        assert all(isinstance(x, str) for x in result)
        lengths = [len(x) for x in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_most_words_and_longest(self, tags_instance):
        n = 5
        result = tags_instance.most_words_and_longest(n)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)

    def test_most_popular(self, tags_instance):
        n = 5
        result = tags_instance.most_popular(n)
        assert isinstance(result, dict)
        assert len(result) == n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_tags_with(self, tags_instance):
        test_word = "action"
        result = tags_instance.tags_with(test_word)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)
        assert all(test_word.lower() in x.lower() for x in result)

class TestLinks:
    def test_init_data_types(self, links_instance):
        assert isinstance(links_instance.links_dict, dict)
        assert all(isinstance(x, int) or x is None for x in links_instance.links_dict["movieId"])
        assert all(isinstance(x, str) or x is None for x in links_instance.links_dict["imdbId"])
        assert all(isinstance(x, int) or x is None for x in links_instance.links_dict["tmdbId"])

    def test_get_imdb(self, links_instance):
        test_movies = links_instance.links_dict["movieId"][:3]  
        fields = ["Director", "Budget", "Runtime"]
        result = links_instance.get_imdb(test_movies, fields)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, list)
            assert len(item) == len(fields) + 1  
            assert isinstance(item[0], int)  
    def test_top_directors(self, links_instance):
        n = 3
        result = links_instance.top_directors(n)
        assert isinstance(result, list)
        assert len(result) == n
        for director, count in result:
            assert isinstance(director, str)
            assert isinstance(count, int)
        counts = [count for _, count in result]
        assert counts == sorted(counts, reverse=True)

    def test_most_expensive(self, links_instance):
        n = 3
        result = links_instance.most_expensive(n)
        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, str) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_most_profitable(self, links_instance):
        n = 3
        result = links_instance.most_profitable(n)
        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_longest(self, links_instance):
        n = 3
        result = links_instance.longest(n)
        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_top_cost_per_minute(self, links_instance):
        n = 3
        result = links_instance.top_cost_per_minute(n)
        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
        values = list(result.values())
        assert values == sorted(values, reverse=True)