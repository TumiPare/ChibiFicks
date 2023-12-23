import anipy_cli

class AnimeAPI:
    def __init__(self):
        self.entry = None
        self.search_results = None

    def search(self, name):
        '''
        Search for an anime
        returns a tuple of the anime name list and the url list
        '''
        self.entry = anipy_cli.Entry()
        self.search_results =  anipy_cli.query(name, self.entry).get_links()
        return self.search_results

    def get_ep_range(self):
        '''
        Returns the range of episodes for the selected show
        '''
        handler = anipy_cli.epHandler(self.entry)
        self.entry.latest_ep = handler.get_latest()
        return (int(handler.get_first()),int(self.entry.latest_ep))
    
    def select_show(self, index):
        '''
        Selects the show from the search results
        '''
        self.entry.category_url = "https://gogoanime.gg/" + self.search_results[0][index]
        self.entry.show_name = self.search_results[1][index]
    
    def get_show_name(self):
        '''
        Returns the name of the selected show
        '''
        return self.entry.show_name
        
    def select_episode(self, episode_num):
        '''
        Selects the episode from the selected show
        '''
        self.entry.ep = episode_num

    def get_link(self):
        '''
        Returns the link to the episode
        '''   
        self.entry = anipy_cli.epHandler(self.entry).gen_eplink()
        url_parser = anipy_cli.url_handler.videourl(self.entry, 'auto')
        url_parser.stream_url()
        self.entry = url_parser.get_entry()
        return self.entry.stream_url
    


def main():
    search = input("Search: ")
    api = AnimeAPI()
    search_results = api.search(search)
    for i, name in enumerate(search_results[1]):
        print(f"[{i}]: {name}")

    show = int(input("Select show: "))
    api.select_show(show)
    range = api.get_ep_range()
    episode = int(input(f"Select episode [{range[0]},{range[1]}]: "))
    api.select_episode(episode)

    print(api.get_link())

if __name__ == "__main__":
    main()
