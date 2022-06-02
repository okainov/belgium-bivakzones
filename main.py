import re

import requests

GPX_HEAD = """<?xml version="1.0" encoding="utf-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="1.0" creator="bivakzone.be" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" xmlns="http://www.topografix.com/GPX/1/0">
"""
GPX_FOOTER = """</gpx>"""

if __name__ == '__main__':
    url = 'https://bivakzone.be/overzichtskaart.html'
    raw_html = requests.get(url).text

    final_gpx = GPX_HEAD
    campsite_matches = re.findall('var titlePlacemark.*?= "(.*?)".*?LatLng\((.*?), (.*?)\).*?href="(.*?)"', raw_html,
                                  flags=re.DOTALL)
    for name, lat, lon, partial_url in campsite_matches:
        lat = lat.strip()
        lon = lon.strip()
        # Workarounds due to bad and explicitly incorrect coordinates for some points:
        if 'Torvtak' in name:
            # https://goo.gl/maps/Gnji9z1jzynEWwXe7
            lat = 50.36906631924759
            lon = 5.118701374634393
        elif 'Levitas' in name:
            # https://goo.gl/maps/hRG2ZWoNVhzqtrdc7
            lat = 50.31843732010222
            lon = 5.077592705678853
        elif 'son aile' in name:
            # https://goo.gl/maps/YtDhxZTT2NZREiKo9
            lat = 50.44621435740369
            lon = 5.068159432619653
        elif 'Trivouac' in name:
            # https://goo.gl/maps/CKaSypmG5CRkmdh56
            lat = 50.42672086992455
            lon = 5.196808815316432
        elif 'Abri Tout' in name:
            # https://goo.gl/maps/h1VjYtV3juannMXr9
            lat = 50.338030953168854
            lon = 5.276097510746715
        elif 'Cubique' in name:
            # https://goo.gl/maps/jMPR3NX4hFydXqad6
            name += ' (closed?)'
            lat = 50.283621361480904
            lon = 5.25936116348321
        elif 'Triskele' in name:
            # https://sentiersdart.be/oeuvres/trisekele
            lat = 50.40349346739489
            lon = 5.0652749477697405

        final_gpx += f"""
<wpt lat="{lat}" lon="{lon}">
    <name>{name}</name>
    
    <desc>https://bivakzone.be{partial_url}

See full map at https://bivakzone.be/overzichtskaart.html.
    </desc>
    <src>https://bivakzone.be{partial_url}</src>
    
    <extensions>
        <locus:icon>tourism-campingsite.png</locus:icon>
    </extensions>
</wpt>"""
    final_gpx += GPX_FOOTER
    with open('bivakzones.gpx', 'w', encoding='UTF-8') as f:
        f.write(final_gpx)

    print(
        f'Successfully parsed and written {len(campsite_matches)} bivak zones from https://bivakzone.be to bivakzones.gpx')
