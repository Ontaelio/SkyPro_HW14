from flask import Flask, jsonify, abort

from utils import *

app = Flask(__name__)


@app.route("/movie/<title>")
def api_get_one_movie(title):
    return jsonify(get_single_movie_by_title(title))


@app.route("/movie/<int:year_one>/to/<int:year_two>")
def api_get_movies_by_years(year_one, year_two):
    return jsonify(get_movies_by_year_range(year_one, year_two))


@app.route("/rating/<rating>")
def api_get_movies_by_rating(rating):
    if rating == 'children':
        return jsonify(get_movies_by_rating('G', 'placeholder'))
        # I prefer a 'placeholder' here instead of two requests with an if clause in the function
    if rating == 'family':
        return jsonify(get_movies_by_rating('G', 'PG', 'PG-13'))
    if rating == 'adult':
        return jsonify(get_movies_by_rating('R', 'NC-17'))
    abort(404, 'No such rating')


@app.route("/genre/<genre>")
def api_get_movies_by_genre(genre):
    return jsonify(get_movies_by_genre(genre))


if __name__ == '__main__':
    app.run()
