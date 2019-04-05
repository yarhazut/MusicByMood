from LastFm.lastFmTags import lastfm_tagsOfSongs_search, get_tags_Array
import json


def create_posting_for_lastfm():
    max_tag = 0;
    counter = 0;
    path_for_songs = "C:\\all_songs\\all_songs.txt"
    path_for_tags_vectors = "C:\\lastFM\\songs_tags_vactors.txt"
    f_songs = open(path_for_songs)
    # foreach song
    for line in f_songs:
        try:
            song_obj = json.loads(line)
            song_name = song_obj['songName']
            song_artist = song_obj['artist']
            # get the last.fm tags
            song_tags = lastfm_tagsOfSongs_search(song_artist, song_name);
            song_tags_arr = get_tags_Array(song_tags)
            if len(song_tags_arr) > 0:
                counter = counter + 1
                # create tags vector for each song: tag + count
                tags_dic = {}
                for tagObject in song_tags_arr:
                    # TODO: if the tag is in the clustered tags (after cleaning)
                    # get rid of tags with artist\song name
                    if song_artist.lower() != tagObject['name'] and song_name.lower() != tagObject['name']:
                        if tagObject['count'] > max_tag:
                            max_tag = tagObject['count']
                        tags_dic[tagObject['name']] = tagObject['count']
                # normalize the count for each tag of a specific song
                for tag_name, tag_count in tags_dic.items():
                    tags_dic[tag_name] = float(float(tag_count) / max_tag)
                song_tags_vector = {'songName': song_name, 'songArtist': song_artist, 'tagsVector': tags_dic}
                with open(path_for_tags_vectors, 'a') as outfile:
                    json.dump(song_tags_vector, outfile)
                    outfile.write('\n')
                print(counter)
        except Exception:
            pass


def padVectorsForSameFormat():
    path = "C:\\lastFM\\songs_tags_vactors.txt"
    padded_vectors_arr= [];
    f = open(path)
    all_tags = readAllClustersFromText()
    #iterate the songs' vectors from last.fm
    for line in f:
        lastfm_song_vector_obj = json.loads(line)
        song_name = lastfm_song_vector_obj['songName']
        song_artist = lastfm_song_vector_obj['songArtist']
        tags_dic = lastfm_song_vector_obj['tagsVector']
        for song_vector in tags_dic:
            for tag in all_tags:
            if (tags_dic[tag]!= null)
                padded_vectors_arr


def readAllClustersFromText():
    path = "C:\\Users\yarha\\Desktop\\clusters\\clusters_350.txt"
    lines = [line.rstrip('\n') for line in open(path)]
    for line in lines:
        if line.isspace():
            lines.remove(line)
    return lines;










create_posting_for_lastfm();
