import myanimelist.session
import time

FILENAME = "dump.txt"

def main():
    s = myanimelist.session.Session()
    with open(FILENAME, 'a') as f:
        for i in range(10, 100):
            try:
                anime = s.anime(i)
                title = anime.title
                voice_actors = ",".join([str(person.id) for person in anime.voice_actors.keys()])
                staff = ",".join([str(person.id) for person in anime.staff.keys()])
                genres = ",".join(anime.genres)
                # Extract the id part of the recommendation
                recommendations = ",".join([str(rec[0].split('/')[2]) for rec in anime.recommendations])
                rec_count = ",".join([str(rec[1]) for rec in anime.recommendations])
                f.write("|".join([str(i), title, voice_actors, staff, genres, recommendations, rec_count]))
                f.write("\n")
                time.sleep(1)
            except:
                print "got fucked"

if __name__ == "__main__":
    main()
