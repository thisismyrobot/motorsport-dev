import urllib2


class GoogleMap(object):
    """ returns an image from a coordinate
    """
    def get_img(self, lat, lng, width, height):
        url = "http://maps.google.com/mapdata?latitude_e6=4251990545&longitude_e6=147308293&zm=500&w=%s&h=%s&cc=&min_priority=2" % (width, height)
        request = urllib2.Request(url)
        connection = urllib2.urlopen(request)
        image = connection.read()
        connection.close()
        return image