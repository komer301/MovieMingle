from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from backend import movie_data
import urllib.parse
from . import db
from .models import Watchlist
import json

views = Blueprint("views", __name__)

@views.route('/movies', methods=['POST', 'GET'])
@login_required
def movies():
    if request.method == 'POST':
        title = request.form.get('searchbar')
        return redirect(url_for('views.search', title=title))  
    data = movie_data.trendingInfo("movie", "week")[:12]
    upcoming = movie_data.upcomingInfo("movie")[:12]
    return render_template("movies.html", data=data, upcoming=upcoming)

@views.route('/tvshows', methods=['POST', 'GET'])
@login_required
def tvshows():
    if request.method == 'POST':
        title = request.form.get('searchbar')
        return redirect(url_for('views.search', title=title)) 
    data = movie_data.tvShowTrending()[:12]
    return render_template("tvshows.html", data=data)

@views.route('/watchlist', methods=['POST', 'GET'])
@login_required
def watchlist():
    if request.method == 'POST':
        title = request.form.get('searchbar')
        return redirect(url_for('views.search', title=title))
    shows = Watchlist.query.filter_by(user_id=current_user.id).all()
    movie_ids = [show.movie_id for show in shows]
    data = movie_data.tvShowTrending()[:12]
    return render_template("tvshows.html", data=data)

@views.route('/search/<title>', methods=['POST', 'GET'])
@login_required
def search(title):
    if request.method == 'POST':
        title = request.form.get('searchbar')
        return redirect(url_for('views.search', title=title)) 
    title = urllib.parse.unquote(title)
    data = movie_data.multiSearch(title)
    return render_template("search.html", data=data, name=title)

@views.route('/add-watchlist',methods=['POST'])
def add_watchlist():
    show = json.loads(request.data)
    showId = show['ShowId']
    show = Watchlist.query.filter_by(movie_id=showId).first()
    if show == None:
        show = Watchlist(movie_id = showId, user_id= current_user.id)
        db.session.add(show)
        db.session.commit()
    return jsonify({})
    
@views.route('/remove-watchlist',methods=['POST'])
def remove_watchlist():
    show = json.loads(request.data)
    showId = show['ShowId']
    show = Watchlist.query.filter_by(movie_id=showId,user_id=current_user.id).first()
    if show:
        db.session.delete(show)
        db.session.commit()
    return jsonify({})
    