music = {
    "pakistan": "https://www.youtube.com/watch?v=1XOJFuKHCck&list=RD1XOJFuKHCck&start_radio=1&pp=ygUFZmE5bGGgBwE%3D",
    "loss": "https://www.youtube.com/shorts/s66jRABGPcY",
    "mid": "https://www.youtube.com/shorts/2F-v4jPhAaE",
    "Taarak" : "https://www.youtube.com/watch?v=m-2aFCLUm-s",
    "song":  "https://www.youtube.com/watch?v=kp2OKfe2g0Y&list=RDkp2OKfe2g0Y&start_radio=1&pp=oAcB",
    
}


def get_music_link(song_name):
    song_name = song_name.lower()
    if song_name in music:
        return music[song_name]
    else:
        return None
