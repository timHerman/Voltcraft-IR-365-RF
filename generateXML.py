__author__ = 'tim'

from lib.log365rf import Log365RF
import os

""" serialize was stolen from http://www.madchicken.it/2010/06/serialize-a-python-dictionary-to-xml.html """
def serialize(root):
    xml = ''
    for key in root.keys():
        if isinstance(root[key], dict):
            xml = '%s<%s>\n%s</%s>\n' % (xml, key, serialize(root[key]), key)
        elif isinstance(root[key], list):
            xml = '%s<%s>' % (xml, key)
            for item in root[key]:
                xml = '%s%s' % (xml, serialize(item))
            xml = '%s</%s>' % (xml, key)
        else:
            value = root[key]
            xml = '%s<%s>%s</%s>\n' % (xml, key, value, key)
    return xml

if __name__ == '__main__':
    l = Log365RF()

    filename = 'data.xml'
    data = l.getData()

    file = open(filename, 'wb')
    file.write(serialize(data))
    file.close()

