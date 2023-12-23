from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from .anime_api import AnimeAPI

api = AnimeAPI()
# Create your views here.
def home(request):
    # template = loader.get_template('anime/index.html')
    # return HttpResponse(template.render())
    

     # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        context = {}
        search_query = request.POST['search_query']
        # Filter your model by the search query
        search_results = api.search(search_query)
        if(search_results):
            context["names"] = search_results[1]
        else:
            context["error"] = "No Results Found"
        return render(request, 'anime/index.html', context)
    else:
        return render(request, 'anime/index.html',{})

def open_player(request):
        index = request.GET.get('index')
        api.select_show(int(index))

        start, end = api.get_ep_range()

        context = {"name:" : api.get_show_name(), "ep_range": range(start, end + 1)}
        return render(request, 'anime/player.html', context)
    
def open_episode(request):
    
    episode = request.GET.get('episode')
    print("episode: ", episode)
    api.select_episode(episode)
    context = {
            "name:" : api.get_show_name(), 
            "ep_range": api.get_ep_range(),
            "link": api.get_link()
    }
    
    return render(request, 'anime/player.html', context)

