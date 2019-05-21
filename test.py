from core import tags, config, lastfm, CONFIG_PATH


#print(tags.getTags("D:\\MUSICA\\Deftones\\[1997] Around the Fur\\02 - Lhabia.mp3"))

titles = [

"korn",
"Korn / Corey Taylor",
"Drowning Pool/Rob Zombie",
"Dope/Zakk Wylde",
"Detroit Hate Choir/Dope",
"Breaking Benjamin/Sebastian Davin",
"Ac/Dc",
"(Hed) P.E./Morgan Lander/Serj Tankian",
"(Hed) P.E./East Bay Ray",
"(Hed) P.E./(Hed) Pe Ft. Big B",
"(Hed) P.E./(Hed) P.E. Ft. The Dirtball",
"(Hed) P.E./(Hed) P.E. Ft. Tech N9Ne",
"(Hed) P.E./(Hed) P.E. Ft. Potluck",
"(Hed) P.E./(Hed) P.E. Ft. Kottonmouth Kings"
]


def cleanArtist(artist):
    val = artist.split("/")[0]
    val = val.rstrip()
    return val
""" 
for t in titles:
    print(cleanArtist(t)) """


print(lastfm.getAlbumInfo("Lenny Kravitz", "Mama Said"))

