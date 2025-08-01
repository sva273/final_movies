# Импорт функций для поиска
from final_movies.all_searches import (
    search_by_keyword_workflow,  # Поиск по ключевому слову
    search_by_genre_and_year_workflow,  # Поиск по жанру и диапазону лет
    search_by_rating_workflow,  # Поиск по рейтингу MPAA
)

# Импорт функций для отображения логов и статистики
from final_movies.log_stats import (
    display_top_searches,  # Отображение самых популярных запросов
    display_last_unique_searches,  # Отображение последних уникальных запросов
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
        try:
            choice = input("Select an option (1-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nInput interrupted. Exiting Movie Finder. Goodbye!")
            break

        if choice == "1":
            # Запуск поиска по ключевому слову
            search_by_keyword_workflow()
        elif choice == "2":
            # Запуск поиска по жанру и диапазону лет
            search_by_genre_and_year_workflow()
        elif choice == "3":
            # Запуск поиска по рейтингу MPAA
            search_by_rating_workflow()
        elif choice == "4":
            # Подменю логов поиска
            while True:
                print("\n=== Search Activity Menu ===")
                print("1. Show TOP 5 Popular Searches")
                print("2. Show 5 Last Unique Searches")
                print("3. Back to Main Menu")

                try:
                    sub_choice = input("Select an option (1-3): ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nInput interrupted. Returning to Main Menu.")
                    break

                if sub_choice == "1":
                    # Показать топ 5 популярных поисков
                    display_top_searches()
                elif sub_choice == "2":
                    # Показать 5 последних уникальных поисков
                    display_last_unique_searches()
                elif sub_choice == "3":
                    # Вернуться в главное меню
                    break
                else:
                    # Обработка неверного ввода
                    print("Invalid option. Please try again.")
        elif choice == "5":
            # Завершение программы
            print("Exiting Movie Finder. Goodbye!")
            break
        else:
            # Обработка неверного ввода
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
