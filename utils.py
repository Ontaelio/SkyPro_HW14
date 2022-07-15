import sqlite3
from json import JSONEncoder


def get_data(query: str, substrings=None, base="netflix.db"):
    """
    get data from SQL
    :param query: query string
    :param substrings: substrings dict
    :param base: database name
    :return:
    """

    if not substrings:
        substrings = {}

    with sqlite3.connect(base) as the_base:
        cursor = the_base.cursor()
        cursor.execute(query, substrings)
        return cursor.fetchall()


def get_single_movie_by_title(title: str) -> dict:
    """
    Task 1 - get a single movie by the title, newest preferred if titles identical
    :param title: movie title or part thereof
    :return: a single database entry as a dict
    """

    sub_str = {"movie_title": f"%{title}%"}

    q = """
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title LIKE :movie_title
            ORDER BY release_year DESC
            LIMIT 1
    """

    raw_data = get_data(q, sub_str)
    if raw_data:
        return {"title": raw_data[0][0],
                "country": raw_data[0][1],
                "release_year": raw_data[0][2],
                "genre": raw_data[0][3],
                "description": raw_data[0][4],
                }
    return {}


def get_movies_by_year_range(start_year: int, end_year: int) -> list:
    """
    Task 2: get 100 (max) movies released between start_year and end_year
    :param start_year:
    :param end_year:
    :return: a list of movies
    """

    sub_str = {"start_year": str(start_year),
               "end_year": str(end_year)}

    q = """
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN :start_year AND :end_year
            ORDER BY release_year
            LIMIT 100
    """

    raw_data = get_data(q, sub_str)
    return_data = []

    if raw_data:
        for item in raw_data:
            return_data.append({"title": item[0],
                                "release_year": item[1]
                                })

    return return_data


def get_movies_by_rating(*rating) -> list:
    """
    Task 3: get movies with ratings listed in *rating
    :param rating: rating strings as *args (at least two!)
    :return: a list of movies, max 100
    """

    sub_str = {"rating_needed": f'{rating}'}
    # No idea why this doesn't work, while the same f-string inserted in the query does.
    # However, using an f-string here is safe, as it is composed inside the view

    q = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN {rating}
            LIMIT 100
    """

    raw_data = get_data(q, sub_str)
    return_data = []

    if raw_data:
        for item in raw_data:
            return_data.append({"title": item[0],
                                "rating": item[1],
                                "description": item[2],
                                })

    return return_data


def get_movies_by_genre(genre: str) -> list:
    """
    Task 4: get 10 most recent movies of a specific genre
    :param genre: the genre to search
    :return: a list of 10 movies
    """

    sub_str = {"genre": f'%{genre}%'}

    q = """
            SELECT title, description, release_year, listed_in
            FROM netflix
            WHERE listed_in LIKE :genre
            ORDER BY release_year DESC
            LIMIT 10
    """

    raw_data = get_data(q, sub_str)
    return_data = []

    if raw_data:
        for item in raw_data:
            return_data.append({"title": item[0],
                                "description": item[1],
                                })

    return return_data


def get_actors_by_actors_pair(actor1: str, actor2: str) -> list:
    """
    Task 5, part 1: get casts lists of all movies where both actors are present
    :param actor1:
    :param actor2:
    :return: a list of casts
    """
    sub_str = {"first_actor": f'%{actor1}%',
               "second_actor": f'%{actor2}%'}

    q = """
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE :first_actor
            AND "cast" LIKE :second_actor
    """

    raw_data = get_data(q, sub_str)

    return raw_data


def find_third_actor(actors_list: list, *actors_to_pair):
    """
    Task 5, part 2: Finds all actors that were in more than 2 movies with the other one(s)
    (not necessarily 'third ones', as I changed the second and third args to *args)
    :param actors_list: a list of movie casts
    :param actors_to_pair: 'the other ones'
    :return: a list of actors seen more than twice
    """

    actors_all = []

    for movie in actors_list:
        actors = movie[0].split(", ")
        actors_all.extend(actors)

    actors_seen_thrice = {actor for actor in actors_all if actors_all.count(actor) > 2} - set(actors_to_pair)
    return list(actors_seen_thrice)


def get_movies_by_type_year_genre(m_type: str, year: int, genre: str) -> list:
    """
    Task 6: get all the movies/TV Shows of a specified genre released in 'year'
    :param m_type: movie or tv show
    :param year:
    :param genre:
    :return: a list of movies/shows
    """
    sub_str = {"m_type": f'%{m_type}%',
               "year": year,
               "genre": f'%{genre}%'}

    q = """
            SELECT title, description, "type", release_year, listed_in
            FROM netflix
            WHERE listed_in LIKE :genre
            AND release_year = :year
            AND "type" LIKE :m_type
    """

    raw_data = get_data(q, sub_str)

    return JSONEncoder().encode(raw_data)


if __name__ == '__main__':

    # demos for functions without views

    # task 6
    ya = get_movies_by_type_year_genre('Movie', 2010, 'Sci-fi')
    print(ya)

    # task 5
    casts = get_actors_by_actors_pair('Jack Black', 'Dustin Hoffman')
    print(find_third_actor(casts, 'Jack Black', 'Dustin Hoffman'))

    casts = get_actors_by_actors_pair('Rose McIver', 'Ben Lamb')
    print(find_third_actor(casts, 'Rose McIver', 'Ben Lamb'))

    casts = get_actors_by_actors_pair('Adam Sandler', 'Rob Schneider')
    print(find_third_actor(casts, 'Adam Sandler', 'Rob Schneider'))

    casts = get_actors_by_actors_pair('John Paul Tremblay', 'Robb Well')
    print(find_third_actor(casts, 'John Paul Tremblay', 'Robb Well'))



