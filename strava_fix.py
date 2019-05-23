import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime,timedelta
from datetime import tzinfo
import dateutil.parser
# from dateutil import tz as TZ
# tree = ET.parse("Ioane_run_4.gpx")
# root = tree.getroot()
# print(root.tag)
# print(root.attrib)
# print("----------------------")
# track = root.find("{http://www.topografix.com/GPX/1/1}trk")
# trkseg = track.find('{http://www.topografix.com/GPX/1/1}trkseg')

def getTrkSeg(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    track = root.find("{http://www.topografix.com/GPX/1/1}trk")
    trkseg = track.find('{http://www.topografix.com/GPX/1/1}trkseg')
    return trkseg
def trkSeg2np(trkseg):
    segs = len(trkseg)
    data = np.zeros([segs,4])
    for i,child in enumerate(trkseg):
        data[i,0] = child.attrib['lat']
        data[i,1] = child.attrib['lon']
        elevElement = child[0] 
        timeElement = child[1]
        date = timeElement.text
        seconds,tz = convert2number(date)
        data[i,2] = elevElement.text
        data[i,3] = seconds
    return data
def convert2number(time):
    time2 = dateutil.parser.parse(time)
    tz = time2.tzinfo
    time_temp = datetime(1970,1,1,tzinfo=tz)
    delta1 = (time2-time_temp).total_seconds()
    total_seconds = (time2-time_temp).total_seconds()
    return total_seconds,tz
def convert2time(total_seconds,tz):
    delta = timedelta(seconds=total_seconds)
    time = delta+datetime(1970,1,1,tzinfo = tz)
    return time
def grab_outlier(data):
    grads = np.gradient(data,axis=0)
    grads[:,0] = grads[:,0] / grads[:,3]
    grads[:,1] = grads[:,1] / grads[:,3]
    dLats = np.abs(grads[:,0])
    dLons = np.abs(grads[:,1])
    dMan = dLons + dLats
    indexes = dMan > .0002
    # for i,d,grad in zip(indexes,dMan,grads):
    #     print(i,'%f' % d,'%f,%f,%f,%f' % (grad[0],grad[1],grad[2],grad[3]))
    return np.where(indexes==True)
    # return indexes


def main():
    # temp = "2019-05-02T02:34:38Z"
    trkseg = getTrkSeg("Ioane_run_4.gpx")
    data = trkSeg2np(trkseg)
    locs = grab_outlier(data)
    print(locs)



if __name__== "__main__":
    main()