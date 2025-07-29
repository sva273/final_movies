# Импорт функций для поиска
from final_movies.all_searches import (
    search_by_keyword_workflow,
    search_by_genre_and_year_workflow,
    search_by_rating_workflow,
)

# Импорт функций для отображения логов и статистики
from final_movies.log_stats import (
    display_top_searches,
    display_last_unique_searches,
    display_last_rating_searches,
)


# Главная точка входа — меню поиска фильмов
def main() -> None:
    """
    Запускает главное интерактивное меню поиска фильмов.

    Пользователь может выбирать различные варианты поиска,
    просматривать статистику поисковых запросов или выйти из программы.

    Обрабатывает исключения для предотвращения аварийного завершения,
    выводя информативные сообщения об ошибках.
    """
    while True:
        # Главное меню
        print("\n=== Movie Finder ===")
        print("1. Search movies by keyword")
        print("2. Search movies by genre and year range")
        print("3. Search movies by MPAA rating")
        print("4. Show search activity")
        print("5. Exit")

        # Получение пользовательского выбора
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            search_by_keyword_workflow()
        elif choice == "2":
            search_by_genre_and_year_workflow()
        elif choice == "3":
            search_by_rating_workflow()
        elif choice == "4":
            # Подменю логов поиска
            while True:
                print("\n=== Search Activity Menu ===")
                print("1. Show TOP 5 Popular Searches")
                print("2. Show 5 Last Unique Searches")
                print("3. Show 5 Last MPAA rating Searches")
                print("4. Back to Main Menu")

                sub_choice = input("Select an option (1-4): ").strip()

                if sub_choice == "1":
                    display_top_searches()
                elif sub_choice == "2":
                    display_last_unique_searches()
                elif sub_choice == "3":
                    display_last_rating_searches()
                elif sub_choice == "4":
                    # Вернуться в главное меню
                    break
                else:
                    print("Invalid option. Please try again.")
        elif choice == "5":
            print("Exiting Movie Finder. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
