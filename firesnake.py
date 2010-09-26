from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish, xpath
from twisted.internet import reactor
from appscript import *
import random
        
def authd(xmlstream):
    print "connected"

    presence = domish.Element(('jabber:client','presence'))
    xmlstream.send(presence)
    
    xmlstream.addObserver('/message/event/items/item', location_update)

def location_update(elem):
    for item in xpath.queryForNodes("/message/event/items/item", elem):
        user = xpath.queryForNodes("//user", item)[0]
        location = xpath.queryForNodes("//location", item)[0]
        coords = str(location.box).split(" ")
        print "%s has moved to %s" % (user['token'], str(location.__getattr__('name')))
        y = (float(coords[0]) + float(coords[2])) / 2
        x = (float(coords[1]) + float(coords[3])) / 2

        app("Google Earth").SetViewInfo({
            k.latitude:  y,
            k.longitude: x,
            k.distance: random.randint(5000, 30000),
            k.azimuth: random.randint(0, 359),
            k.tilt:    random.randint(0, 75),
        }, speed=1)
    
myJid = jid.JID('jid@jabber.org/twisted_words')
factory = client.basicClientFactory(myJid, 'password')
factory.addBootstrap('//event/stream/authd', authd)
reactor.connectTCP('jabber.org', 5222, factory)
reactor.run()

