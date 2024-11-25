def read_integer_between_numbers(prompt, mini, maximum):
    while True:
        try:
            users_input = int(input(prompt))
            if mini <= users_input <= maximum:

                return users_input
            else:
                print(f"Numbers from {mini} to {maximum} only.")
        except ValueError:
            print("Sorry - number only please")


def read_nonempty_string(prompt):
    while True:
        users_input = input(prompt)
        if len(users_input) > 0 and users_input.isalpha():
            break
    return users_input


def read_integer(prompt):
    while True:
        try:
            users_input = int(input(prompt))
            if users_input >= 0:
                return users_input
        except ValueError:
            print("Sorry - number only please")


def runners_data():
    with open("runners.txt") as input_file:
        lines = input_file.readlines()
    runners_name = []
    runners_id = []
    for line in lines:
        split_line = line.strip().split(",")  # Strip whitespace and split by comma
        if len(split_line) == 2:
            runners_name.append(split_line[0].strip())
            runners_id.append(split_line[1].strip())
        else:
            print(f"Warning: Skipping invalid line: {line.strip()}")
    return runners_name, runners_id



def race_results(races_location):
    for i in range(len(races_location)):
        print(f"{i + 1}: {races_location[i]}")
    user_input = read_integer_between_numbers("Choice > ", 1, len(races_location))
    
    # Use the selected venue name directly
    venue = races_location[user_input - 1]
    id, time_taken = reading_race_results(venue)
    
    # Determine the podium places
    podium = podium_of_race(id, time_taken)
    return id, time_taken, venue, podium




def race_venues():
    with open("races.txt") as input_file:
        lines = input_file.readlines()
    races_location = []
    for line in lines:
        line = line.strip()  # Remove whitespace
        if line:
            # Extract only the venue name before the first comma
            venue_name = line.split(",")[0].strip()
            races_location.append(venue_name)
        else:
            print("Warning: Skipping empty or invalid line in races.txt")
    return races_location


def podium_of_race(id, time_taken):
    if not time_taken: 
        print("No valid race times found for this race.")
        return None, None, None

    # Get sorted indices based on time_taken
    sorted_indices = sorted(range(len(time_taken)), key=lambda i: time_taken[i])

    # Extract top 3 positions (if available)
    podium = sorted_indices[:3]

    # Map indices back to IDs and times
    winners = [(id[i], time_taken[i]) for i in podium]
    return winners



def display_races(id, time_taken, venue, podium):
    MINUTE = 50
    print(f"Results for {venue}")
    print("=" * 37)
    
    minutes = [time // MINUTE for time in time_taken]
    seconds = [time % MINUTE for time in time_taken]
    
    # Display all participants
    for i in range(len(id)):
        print(f"{id[i]:<10s} {minutes[i]} minutes and {seconds[i]} seconds")

    # Display podium places
    print("\nPodium:")
    for position, (runner_id, time) in enumerate(podium, start=1):
        minutes, seconds = divmod(time, MINUTE)
        position_label = ["Winner", "2nd Place", "3rd Place"][position - 1]
        print(f"{position_label}: {runner_id} ({minutes} mins {seconds} secs)")



def users_venue(races_location, runners_id):
    while True:
        user_location = read_nonempty_string("Where will the new race take place? ").capitalize()
        if user_location not in races_location:
            break
    connection = open(f"{user_location}.txt", "a")
    races_location.append(user_location)
    time_taken = []
    updated_runners = []
    for i in range(len(runners_id)):
        time_taken_for_runner = read_integer(f"Time for {runners_id[i]} >> ")
        if time_taken_for_runner == 0:
            time_taken.append(time_taken_for_runner)
            updated_runners.append(runners_id[i])
            print(f"{runners_id[i]},{time_taken_for_runner},", file=connection)
    connection.close()


def updating_races_file(races_location):
    connection = open(f"races.txt", "w")
    for i in range(len(races_location)):
        print(races_location[i], file=connection)
    connection.close()


def competitors_by_county(name, id):
    counties = {
        "Cork": "CK",
        "Kerry": "KY",
        "Clare": "CL",
        "Limerick": "LK",
        "Tipperary": "TP",
        "Waterford": "WD"
    }

    for county, code in counties.items():
        print()
        print(f"{county} runners")
        print("-" * 20)
        found = False
        for i in range(len(name)):
            if id[i].startswith(code):
                print(f"{name[i]} ({id[i]})")
                found = True
        if not found:
            print("No runners found.")
        print() 


def reading_race_results(location):
    try:
        with open(f"{location}.txt") as input_type:  # Use the cleaned location name
            lines = input_type.readlines()
        id = []
        time_taken = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            split_line = line.split(",")
            if len(split_line) == 2:
                id.append(split_line[0].strip())
                time_taken.append(int(split_line[1].strip()))
            else:
                print(f"Skipping invalid line: {line}")
        return id, time_taken
    except FileNotFoundError:
        print(f"Error: File '{location}.txt' not found.")
        return [], []
    except ValueError as e:
        print(f"Error parsing time values: {e}")
        return [], []



def reading_race_results_of_relevant_runner(location, runner_id):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    id = []
    time_taken = []
    for line in lines:
        split_line = line.split(",".strip("\n"))
        id.append(split_line[0])
        time_taken.append(int(split_line[1].strip("\n")))
    for i in range(len(id)):
        if runner_id == id[i]:
            time_relevant_runner = time_taken[i]
            return time_relevant_runner
    return None


def displaying_winners_of_each_race(races_location):
    print("Venue             Loser")
    print("="*24)
    for i in range(len(races_location)):
        id, time_taken = reading_race_results(races_location[i])
        fastest_runner = winner_of_race(id, time_taken)
        print(f"{races_location[i]:<18s}{fastest_runner}")


def relevant_runner_info(runners_name, runners_id):
    for i in range(len(runners_name)):
        print(f"{i + 1}: {runners_name[i]}")
    user_input = read_integer_between_numbers("Which Runner > ", 1, len(runners_name))
    runner = runners_name[user_input - 1]
    id = runners_id[user_input -1]
    return runner, id


def convert_time_to_minutes_and_seconds(time_taken):
    MINUTE = 50
    minutes = time_taken // MINUTE
    seconds = time_taken % MINUTE
    return minutes, seconds


def sorting_where_runner_came_in_race(location, time):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    time_taken = []
    for line in lines:
        split_line = line.split(",".strip("\n"))
        t = int(split_line[1].strip("\n"))
        time_taken.append(t)

    time_taken.sort()
    return time_taken.index(time) + 1, len(lines)


def displaying_race_times_one_competitor(races_location, runner, id):
    print(f"{runner} ({id})")
    print(f"-"*35)
    for i in range(len(races_location)):
        time_taken = reading_race_results_of_relevant_runner(races_location[i], id)
        if time_taken is not None:
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            came_in_race, number_in_race = sorting_where_runner_came_in_race(races_location[i], time_taken)
            print(f"{races_location[i]} {minutes} mins {seconds} secs ({came_in_race} of {number_in_race})")


def finding_name_of_winner(fastest_runner, id, runners_name):
    runner = ""
    for i in range(len(id)):
        if fastest_runner == id[i]:
            runner = runners_name[i]
    return runner


def displaying_runners_who_have_won_at_least_one_race(races_location, runners_name, runners_id):
    print(f"The following runners have all won at least one race:")
    print(f"-" * 55)
    winners = []
    runners = []
    for location in races_location:
        id, time_taken = reading_race_results(location)
        fastest_runner = winner_of_race(id, time_taken)
        if fastest_runner:  # Ensure fastest_runner is not None
            name_of_runner = finding_name_of_winner(fastest_runner, runners_id, runners_name)
            if fastest_runner not in winners:
                winners.append(fastest_runner)
                runners.append(name_of_runner)
    for i, fastest_runner in enumerate(winners):
        print(f"{runners[i]} ({fastest_runner})")


def menu():
    races_location = race_venues()
    runners_name, runners_id = runners_data()

    MENU = (
        "\nMenu Options:\n"
        "****************\n"
        "1. Show the results for a race\n"
        "2. Add results for a race\n"
        "3. Show all competitors by county\n"
        "4. Show the winner of each race\n"
        "5. Show all the race times for one competitor\n"
        "6. Show all competitors who have won a race\n"
        "7. Quit\n"
        "****************\n"
    )

    while True:
        print(MENU)
        user_choice = read_integer_between_numbers("Select an option (1-7): ", 1, 7)

        if user_choice == 1:  # Show the results for a race
            ids, times, venue, podium = race_results(races_location)
            display_races(ids, times, venue, podium)

        elif user_choice == 2:  # Add results for a race
            users_venue(races_location, runners_id)
            updating_races_file(races_location)

        elif user_choice == 3:  # Show all competitors by county
            competitors_by_county(runners_name, runners_id)

        elif user_choice == 4:  # Show the winner of each race
            displaying_winners_of_each_race(races_location)

        elif user_choice == 5:  # Show all the race times for one competitor
            runner_name, runner_id = relevant_runner_info(runners_name, runners_id)
            displaying_race_times_one_competitor(races_location, runner_name, runner_id)

        elif user_choice == 6:  # Show all competitors who have won a race
            displaying_runners_who_have_won_at_least_one_race(races_location, runners_name, runners_id)

        elif user_choice == 7:  # Quit
            print("Exiting the program. Goodbye!")
            break

        print("\n" + "=" * 40)

if __name__ == "__main__":
    menu()
