from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests


def home(request):
    return render(request, 'home.html')


def user(request):
    if request.method == 'GET':
        username = request.GET['username']
        url = "https://api.github.com/users/"
        details = url+ username
        repos = details + "/repos"
        d = {}

        userPage = "https://github.com/" + username
        try:
            userDetails = requests.get(details).json()
            userRepos = requests.get(repos).json()
            userQuery = [
            {
            'page': userPage,
            'login':userDetails['login'],
            'avatar':userDetails['avatar_url'],
            'repos_num':userDetails['public_repos'],
            'id':userDetails['id'],
            'bio':userDetails['bio']

            }

            ]
            repoQuery = []
            for repos in userRepos:
                r = {}
                r['name'] = repos['name']
                r['url'] = repos['html_url']
                repoQuery.append(r)


            d = {
                'User':userQuery,
                'Repo':repoQuery,
                'Title':userDetails['login']
            }
            return render(request, 'User.html', d)
        except:
            print("Something went wrong")
            messages = "No account with this username !!"
            return render(request, 'User.html', {'message':messages})
