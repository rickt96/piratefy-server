from core import *

scanner = Scanner()
""" songs = [
    "D:\\MUSICA\P.O.D\\2001 - Satellite\\04 - Youth Of The Nation.mp3",
    "D:\\MUSICA\P.O.D\\2001 - Satellite\\02 - Alive.mp3",
    "D:\\MUSICA\P.O.D\\2018 - Circles\\07 Listening for the Silence.mp3"
] """

songs = scanner.getfiles([".mp3"], ["D:\\MUSICA\\American Head Charge"])
for s in songs:
    info = scanner.getsongtags_new(s)
    print(str(info[3]))
    print("========")