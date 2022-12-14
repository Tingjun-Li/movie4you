class Movie:
    def __init__(self, json=None):
        """Initialize a Movie object with json input (a dictionary)"""
        image_url = "https://image.tmdb.org/t/p/w300_and_h450_bestv2"
        self.adult = json.get("adult") or False
        self.backdrop_path = image_url + (json.get("backdrop_path") or "#")
        self.poster_path = image_url + (json.get("poster_path") or "#")
        self.genres = json.get("genres") or []
        self.budget = json.get("budget") or 0
        self.imdb_id = json.get("imdb_id") or "No ID"
        self.list_idx = -1
        self.overview = json.get("overview") or "No Overview"
        self.original_language = json.get("original_language") or "No Language"
        self.title = json.get("title") or json.get("original_title") or "No Title"
        self.release_date = json.get("release_date") or "No Date"
        self.runtime = json.get("runtime") or 0
        self.vote_average = json.get("vote_average") or 0
        self.vote_count = json.get("vote_count") or 0

    def info(self):
        """Return a string of the format: TITLE (YEAR)[RATING]"""
        return f"{self.title} ({self.release_year}) [{self.rating}]"
    
    def is_action(self):
        """Return True if the movie is an action movie"""
        for genre in self.genres:
            if genre["name"] == "Action":
                return True
