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

""" 
print(lastfm.getAlbumInfo("Korn", "follow the leader"))
print(lastfm.getArtistInfo("primer 55")) """


try:
    myfile = open("db\\test_korn.sqlite", "w+") # or "r+", whatever you need
    print("ok")
except IOError:
    print("Could not open file! xxxx")


import sys

def prompt(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {
        "yes": True, "y": True, "si": True, "s":True,
        "no": False, "n": False
        }
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


res = prompt("sono una domanda?")
print(res)