# Crawler takes a given URL and crawls through every link found on the page to a 
# given depth.  Each link discovered is saved and ranked based on the provided 
# ranking algorithm.

# TO-DO Add docstring comments

#hash functions
def hashtable_add(htable,key,value):
    """
    
    """
    hashtable_get_bucket(htable,key).append([key,value])
    return htable  
        
def hashtable_get_bucket(htable,keyword):
    """
    
    """
    return htable[hash_string(keyword,len(htable))]

def hash_string(keyword,buckets):
    """
    
    """
    out = 0
    for s in keyword:
        out = (out + ord(s)) % buckets
    return out

def make_hashtable(nbuckets):
    """
    
    """
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table

#rank algorithm
def compute_ranks(graph):
    """
    
    """
    d = 0.8 #damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
        
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

#web crawler
def get_page(url):
    """
    
    """
    try:
        import urllib
        return(urllib.urlopen(url).read())
    except:
        return('')

def get_next_target(page):
    """
    
    """
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    """
    
    """
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    """
    
    """
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def add_to_index(index,keyword,url):
    """
    
    """
    if keyword in index:
        index[keyword].append(url)
    else:
        # not found, add new keyword to index
        index[keyword] = [url]
        
def add_page_to_index(index,url,content):
    """
    
    """
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def lookup(index, keyword):
    """
    
    """
    if keyword in index:
        return index[keyword]
    else:
        return None

def crawl_web(seed):
    """
    
    """
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            contents = get_page(page)
            add_page_to_index(index, page, contents)
            outlinks = get_all_links(contents)
            graph[page] = outlinks
            union(tocrawl,outlinks)
            crawled.append(page)
    return index, graph

#start crawler
index, graph = crawl_web("http://www.udacity.com/cs101x/urank/index.html")
ranks = compute_ranks(graph)
print ranks
