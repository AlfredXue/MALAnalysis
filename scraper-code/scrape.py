import myanimelist.session
import time

FILENAME = "dump.txt"

def get_anime(i):
    s = myanimelist.session.Session()
    f = open('test-dump', 'a')
    try:
        print "triyng " + str(i)
        anime = s.anime(i)
        title = anime.title.encode('utf-8').strip()
        voice_actors = ",".join([str(person.id) for person in anime.voice_actors.keys()])
        staff = ",".join([str(person.id) for person in anime.staff.keys()])
        genres = ",".join([genre.encode('utf-8').strip() for genre in anime.genres])
        # Extract the id part of the recommendation
        recommendations = ",".join([str(rec[0].split('/')[2]) for rec in anime.recommendations])
        rec_count = ",".join([str(rec[1]) for rec in anime.recommendations])
        print genres
        f.write("|".join([str(i), title, voice_actors, staff, genres, recommendations, rec_count]))
        f.write("\n")
        time.sleep(1)
    except:
        raise
        #print "got fucked"
        #time.sleep(1)

def main():
    s = myanimelist.session.Session()
    missing = open("bro.txt")
    with open(FILENAME, 'a') as f:
        for line in missing.readlines():
        #for i in range(10, 100):
            try:
                i = int(line)
                print "triyng " + str(i)
                anime = s.anime(i)
                title = anime.title.encode('utf-8').strip()
                voice_actors = ",".join([str(person.id) for person in anime.voice_actors.keys()])
                staff = ",".join([str(person.id) for person in anime.staff.keys()])
                genres = ",".join([genre.encode('utf-8').strip() for genre in anime.genres])
                # Extract the id part of the recommendation
                recommendations = ",".join([str(rec[0].split('/')[2]) for rec in anime.recommendations])
                rec_count = ",".join([str(rec[1]) for rec in anime.recommendations])
                f.write("|".join([str(i), title, voice_actors, staff, genres, recommendations, rec_count]))
                f.write("\n")
                time.sleep(1)
            except:
                #raise
                print "got fucked"
                time.sleep(1)

if __name__ == "__main__":
    #get_anime(15775)
    main()
