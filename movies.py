import movie_storage
import random
import matplotlib.pyplot as plt
import Levenshtein
from colorama import Fore, Style
from films_web_generator import update_html_file

def main():
    while True:
        # PRINT THE MAIN MENU
        print(f"{Fore.YELLOW}Menu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Create Rating Histogram")
        print("10. Generate website")
        print("")
        choose_number = int(input(f"{Fore.GREEN}Enter choice (0-10): "))

        # CHOOSE THE NUMBER :
        match choose_number:
            case 0:
                print("Bye!")
                exit()
            case 1:
                print("")
                print_all_movies()
            case 2:
                print("")
                add_new_movie()
            case 3:
                print("")
                delete_movie()
            case 4:
                print("")
                update_movie_rating()
            case 5:
                print("")
                show_stats()
            case 6:
                print("")
                print_random_movie()
            case 7:
                print("")
                search_movie()
            case 8:
                print("")
                sorted_by_rating()
            case 9:
                print("")
                make_histogram()
            case 10:
                print("")
                generate_website()
            case _:
                print("Invalid choice. Please try again.")
        return_to_main()

# RETURN TO MAIN MENU, PRESSING 'ENTER'
def return_to_main():
    print(f"{Style.RESET_ALL}")
    input("Press 'Enter' to continue")
    main()

# PRINT ALL MOVIES
def print_all_movies():
    movies = movie_storage.get_movies()
    print(f"{Style.RESET_ALL}{len(movies)} movies in total")
    for movie, details in movies.items():
        print(f"{movie} ({details['year']}) - {details['rating']}★")

# ADD NEW MOVIE
def add_new_movie():
    title = input("Enter new movie name: ")
    movies = movie_storage.get_movies()
    if title in movies:
        print(f"{Fore.RED}Movie '{title}' already exists!")
        return
    movie_storage.add_movie(title)
    print(f"The movie '{title}' has been added to the list.")

# DELETE MOVIE
def delete_movie():
    title = input("Write the name of the film to delete: ")
    movie_storage.delete_movie(title)

# UPDATE A RATING OF MOVIE
def update_movie_rating():
    title = input("Write the name of the film to update: ")
    movies = movie_storage.get_movies()
    if title in movies:
        new_movie_rating = float(input("Write a new rating for the film (from 1 to 10): "))
        movie_storage.update_movie(title, new_movie_rating)
    else:
        print(f"{Fore.RED}'{title}' doesn’t exist in the database")

# SHOW STATS:
def show_stats():
    movies = movie_storage.get_movies()
    if not movies:
        print(f"{Style.RESET_ALL}No movies found.")
        return

    # Filter out movies with 'N/A' ratings
    valid_movies = [movie for movie in movies.values() if 'rating' in movie and movie["rating"] != 'N/A']

    if not valid_movies:
        print(f"{Style.RESET_ALL}No valid ratings to calculate stats.")
        return

    try:
        sum_of_ratings = sum(float(movie["rating"]) for movie in valid_movies)
        count_of_ratings = len(valid_movies)
        average_rating = round(sum_of_ratings / count_of_ratings, 2)
        print(f"{Style.RESET_ALL}Average rating is approximately {average_rating}★")

        ratings = sorted(float(movie["rating"]) for movie in valid_movies)
        n = len(ratings)
        median_rating = (ratings[n // 2] if n % 2 == 1 else (ratings[n // 2 - 1] + ratings[n // 2]) / 2)
        median_rating = round(median_rating, 2)
        print(f"Median rating is approximately {median_rating}★")

        # Sort movies by rating, handling 'N/A' gracefully
        sorted_movies = sorted(valid_movies, key=lambda movie: float(movie.get('rating', 0)), reverse=True)


        if sorted_movies:
            best_movie = sorted_movies[0].get('title', 'Unknown Title')
            worst_movie = sorted_movies[-1].get('title', 'Unknown Title')
            print(f"The best movie is '{best_movie}' with rating '{sorted_movies[0].get('rating', 'N/A')}'★")
            print(f"The worst movie is '{worst_movie}' with rating '{sorted_movies[-1].get('rating', 'N/A')}'★")

    except ValueError as e:
        print(f"ValueError occurred: {e}")
        print("Failed to calculate statistics due to invalid rating format.")




# RANDOM MOVIE
def print_random_movie():
    movies = movie_storage.get_movies()
    random_movie = random.choice(list(movies.keys()))
    print(f"{Style.RESET_ALL}Random movie: {random_movie} ({movies[random_movie]['year']}) with rating {movies[random_movie]['rating']}★")

# SEARCH MOVIE + wrong spelling
def search_movie():
    part_of_name = input(f"{Fore.GREEN}Write part of the name: ")
    movies = movie_storage.get_movies()
    found = False
    for movie in movies:
        if part_of_name.lower() in movie.lower():
            print(f"{movie} ({movies[movie]['year']}) was found with rating {movies[movie]['rating']}★")
            found = True
    if not found:
        print(f"{Style.RESET_ALL}The movie '{part_of_name}' does not exist. Did you mean:")
        for movie in movies:
            distance = Levenshtein.distance(part_of_name, movie)
            if distance < 5:
                print(f"{movie} ({movies[movie]['year']}) with rating {movies[movie]['rating']}★?")

# SORTING BY RATING
def sorted_by_rating():
    movies = movie_storage.get_movies()
    sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]['rating']), reverse=True)
    for movie, details in sorted_movies:
        print(f"{movie} ({details['year']}) - {details['rating']}★")

# SAVE HISTOGRAM
def make_histogram():
    movies = movie_storage.get_movies()
    values_list = [float(movie["rating"]) for movie in movies.values()]
    plt.xlabel("Rating")
    plt.ylabel("Quantity")
    plt.title("Ratings of Movies")
    plt.hist(values_list, bins=10, edgecolor='black')
    user_save = input("In which file to save the histogram? ")
    plt.savefig(user_save)
    plt.close()  # Close the figure to free up memory
    print(f"Histogram saved as {user_save}")

# GENERATE WEBSITE
def generate_website():
    movies = movie_storage.get_movies()
    update_html_file(movies)  # Generate the HTML file with current movies
    print("Website was generated successfully.")

if __name__ == "__main__":
    main()
