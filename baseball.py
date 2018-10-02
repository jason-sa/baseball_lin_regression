import pickle

def get_boxscore_urls(driver):
    urls = []
    links = driver.find_elements_by_link_text('Boxscore')
    for l in links:
        urls.append(l.get_attribute('href'))
    return urls

def write_pkl(data, name):
    with open('pickles/'+name+'.pkl', 'wb') as picklefile:
        pickle.dump(data, picklefile)
