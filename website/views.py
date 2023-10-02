from flask import Blueprint, render_template
from flask_login import login_required
from backend import movie_data

views = Blueprint("views",__name__)

@views.route('/movies')
@login_required
def movies():
    data = movie_data.trendingInfo("movie","week")[:8]
    upcoming = movie_data.upcomingInfo("movie")[:8]
    return render_template("movies.html", data=data, upcoming=upcoming)

@views.route('/tvshows')
@login_required
def tvshows():
    data = movie_data.tvShowTrending()[:8]
    # upcoming = movie_data.upcomingInfo("tv")[:8]
    return render_template("tvshows.html", data=data)