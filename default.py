# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import urlresolver
import urlparse
#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.gledaionlain'
__Addon = xbmcaddon.Addon(__addon_id__)
searchicon = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/search.png")
folder = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/folder.png")

MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0' #За симулиране на заявка от  компютърен браузър


#Меню с директории в приставката
def CATEGORIES():
        addDir('Търсене на видео','https://gledaionlain.com/?s=',2,searchicon)
        addDir('Всички филми','https://gledaionlain.com/filmi/',1,folder)
        baseurl = 'https://gledaionlain.com'
        req = urllib2.Request(baseurl)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        cr = 0
        match = re.compile('<li class="cat-item cat-item-\d+"><a href="https.+?/genre/(.+?)">(.+?)</a> <span>(.+?)</span>').findall(data)
        for link, zaglavie, broifilmi in match:
         url = baseurl + '/genre/' + link
         title = zaglavie + ' Брой филми: ' + broifilmi
         thumbnail = folder
         addDir(title, url, 1, thumbnail)
         cr = cr + 1


#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('<a href="(.+?)">\n<div class="image">\n<img src="(.+?)".*>\n.*\n.*</b>(.+?)</span>\n.*\n.*\n.*\n.*\n.*>(.+?)</span>\n.*\n(.*)<div').findall(data)
        for link, kartinka, imdb, zaglavie, opisanie in match:
            desc = 'IMDB:' + imdb + '  ' +opisanie
            addLink(zaglavie,link,4,desc,kartinka)
            br = br + 1
            #print 'Items counter: ' + str(br)
        if br > 18: #тогава имаме следваща страница и конструираме нейния адрес
            matchp = re.compile('<div class="nav-previous alignleft"><a href="(https.+?)/page/(.+?)/"></a></div>').findall(data)
            for baseurl,numb in matchp:
             number = 0
             page = int(number)
             currentDisplayCounter = page + int(numb)
             url = baseurl + '/page/' + str(currentDisplayCounter)
             #print 'sledvasta stranica' + url
             thumbnail=folder
             addDir('следваща страница>>'+str(currentDisplayCounter),url,1,thumbnail)


#Търсачка
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Търси..')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')
            searchurl = url + searchText
            searchurl = searchurl.encode('utf-8')
            req = urllib2.Request(searchurl)
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            #print 'request page url:' + url
            data=response.read()
            response.close()
            br = 0 #Брояч на видеата в страницата - 24 за този сайт
            match = re.compile('<a href="(.+?)">\n<div class="image">\n<img src="(.+?)".*>\n.*\n.*</b>(.+?)</span>\n.*\n.*\n.*\n.*\n.*>(.+?)</span>\n.*\n(.*)<div').findall(data)
            for link, kartinka, imdb, zaglavie, opisanie in match:
             desc = 'IMDB:' + imdb + '  ' +opisanie
             addLink(zaglavie,link,4,desc,kartinka)
             br = br + 1


        else:
             addDir('Върнете се назад в главното меню за да продължите','','',"DefaultFolderBack.png")

def SHOW(url):
       url1 = url
       req = urllib2.Request(url)
       req.add_header('User-Agent', UA)
       response = urllib2.urlopen(req)
       data=response.read()
       response.close()
       match = re.compile('<iframe.src="(.+?)" scrolling="no" frameborder="0"').findall(data)
       for link in match:
        print link
        addLink2(name,link,4)







#Зареждане на видео
def PLAY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        match = re.compile('<iframe.src="(.+?)" scrolling="no" frameborder="0"').findall(data)
        for link1 in match:
         url = link1
         li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url)
         li.setInfo('video', { 'title': name })
        link = url
        try: stream_url = urlresolver.HostedMediaFile(link).resolve()
        except:
               deb('Link URL Was Not Resolved',link); deadNote("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL."); return

        ##xbmc.Player().stop()
        play=xbmc.Player() ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''
        play.play(stream_url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''




#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({'thumb': iconimage, 'poster': iconimage, 'banner': iconimage, 'fanart': iconimage})
        liz.setInfo(type="Video", infoLabels={"Title": name, "plot": plot})
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addLink2(name,url,mode,):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({'thumb': iconimage, 'poster': iconimage, 'banner': iconimage, 'fanart': iconimage})
        liz.setInfo(type="Video", infoLabels={"Title": name })
        liz.setProperty("IsPlayable" , "false")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({'thumb': iconimage, 'poster': iconimage, 'banner': iconimage, 'fanart': iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def log(txt, loglevel=xbmc.LOGDEBUG):
    if (__addon__.getSetting( "logEnabled" ) == "true") or (loglevel != xbmc.LOGDEBUG):
        if isinstance (txt,str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (__addonid__, txt)
        xbmc.log(msg=message.encode("utf-8"), level=loglevel)

#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        SEARCH(url)

elif mode==3:
        print ""+url
        SHOW(url)
        
elif mode==4:
        print ""+url
        PLAY(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
