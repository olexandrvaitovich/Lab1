import geocoder
import folium
from geopy import ArcGIS
import html


def read_file(year):
    '''
    (number) -> (list)
    Returns list with tuples of film name and filming place
    '''
    films = set()
    file = open('locations.list', 'r').readlines()
    for i in file:
        if str(year) in i:
            a = i.strip().split('\t')
            f_name = a[0][:a[0].index('{')] if '{' in a[0] else a[0]
            if str(year) in f_name:
                f_name = f_name[:f_name.index('(')] if '(' in a[0] else f_name
                if str(year) not in f_name:
                    films.add(
                        (f_name, a[-1] if '(' not in a[-1] else a[-2]))
    return films


def geolocation(location):
    '''
    (str) -> (list)
    Returns list with latitude and longitude of location
    '''
    geolocator = ArcGIS(timeout=10)
    loc = geolocator.geocode(location)
    return [loc.latitude, loc.longitude]


def f_dict(f_set, f_num):
    f_list = list(f_set)
    f_dict = dict()
    for i in range(f_num):
        if f_list[i][1] in f_dict:
            f_dict[f_list[i][1]].append(f_list[i][0])
        else:
            f_dict[f_list[i][1]] = [f_list[i][0]]
    return f_dict


def wmap(films):
    wmap = folium.Map(location=[45.5236, -122.6750],
                      zoom_start=3, tiles='Mapbox bright')
    fg = folium.FeatureGroup(name="Filming Locations")
    for i in films:
        st=''
        for i in list(map(lambda x: html.escape(x), films[i])):
            st+=i+'\n'
        fg.add_child(folium.Marker(location=geolocation(
            html.escape(i)), popup=st))
    wmap.add_child(fg)
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {'fillColor': 'green'
                                                             if x['properties']['POP2005'] < 10000000
                                                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                             else 'red'}))
    wmap.add_child(fg_pp)
    wmap.add_child(folium.LayerControl())
    wmap.save(outfile='wmap.html')


def main():
    year=int(input('Please input a year: '))
    num=int(input('Please input number of films: '))
    wmap(f_dict(read_file(year),num))
main()
