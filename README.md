# Study Buddy Bot

Study Buddy is a Discord bot designed to help students stay motivated, test their knowledge, and track their study progress. It includes features like study tips, flashcards, quizzes, progress tracking, leaderboards, and study reminders.

## Features
- 📖 **Study Tips**: Get study tips in multiple languages (English, Spanish, French).
- 🎴 **Flashcards**: Add, edit, and quiz yourself on flashcards.
- 🎯 **Quizzes**: Test yourself on different topics with flashcard quizzes.
- 🎮 **Gamification**: Earn points for studying and view the leaderboard.
- ⏰ **Reminders**: Set study reminders to stay on track.
- 📂 **Export Flashcards**: Download your flashcards in JSON or CSV format.

## Commands
| Command | Description |
|---------|-------------|
| `/studytip [topic] [language]` | Get a random study tip in a chosen language. |
| `/addflashcard <topic> <question> <answer> [language]` | Add a new flashcard. |
| `/editflashcard <topic> <question> <new_answer>` | Edit an existing flashcard. |
| `/quiz <topic> [language]` | Start a quiz on a topic. |
| `/progress` | Check your study progress. |
| `/leaderboard` | View the top study performers. |
| `/setreminder <minutes> [topic]` | Set a study reminder. |
| `/export [format]` | Export flashcards in JSON or CSV format. |

## Installation
1. Install Python 3.8+
2. Install dependencies:
   ```sh
   pip install discord pandas
   ```
3. Create a `flashcards.json` and `user_progress.json` file in the project directory.
4. Run the bot:
   ```sh
   python bot.py
   ```

## Configuration
- Make sure to update the bot token inside `bot.py` before running it.
- Add your bot to a Discord server with the required permissions.

## Future Enhancements
- Add more languages for study tips.
- Implement voice-based quizzes.
- Add AI-powered study recommendations.

## Contributing
Feel free to contribute by opening issues and pull requests!

## License
This project is licensed under the MIT License.
