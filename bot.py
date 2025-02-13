import discord
from discord import app_commands
import json
import random
import os
import asyncio
from datetime import datetime
import pandas as pd
from typing import Optional

class StudyBuddyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)
        self.flashcards = {}
        self.user_progress = {}
        self.study_reminders = {}
        self.languages = ['en', 'es', 'fr']  # Supported languages
        self.load_data()

    def load_data(self):
        # Load flashcards
        if os.path.exists('flashcards.json'):
            with open('flashcards.json', 'r', encoding='utf-8') as f:
                self.flashcards = json.load(f)
        
        # Load user progress
        if os.path.exists('user_progress.json'):
            with open('user_progress.json', 'r') as f:
                self.user_progress = json.load(f)

    def save_data(self):
        # Save flashcards
        with open('flashcards.json', 'w', encoding='utf-8') as f:
            json.dump(self.flashcards, f, ensure_ascii=False, indent=2)
        
        # Save user progress
        with open('user_progress.json', 'w') as f:
            json.dump(self.user_progress, f, indent=2)

    def get_user_points(self, user_id: str) -> int:
        return self.user_progress.get(str(user_id), {}).get('points', 0)

    def award_points(self, user_id: str, points: int):
        if str(user_id) not in self.user_progress:
            self.user_progress[str(user_id)] = {'points': 0, 'correct_answers': 0, 'total_answers': 0}
        self.user_progress[str(user_id)]['points'] += points
        self.save_data()

client = StudyBuddyBot()

# Multi-language study tips
STUDY_TIPS = {
    'en': [
        "Break your study sessions into 25-minute chunks with 5-minute breaks.",
        "Review your notes within 24 hours of taking them.",
        "Create mind maps to visualize connections between concepts.",
        "Practice active recall by testing yourself frequently.",
        "Use spaced repetition for long-term retention.",
        "Study in a quiet, well-lit environment to enhance focus.",
        "Drink water and stay hydrated to keep your brain sharp.",
        "Organize your study materials before starting.",
        "Set specific goals for each study session.",
        "Avoid multitasking to maximize efficiency."
    ],
    'es': [
        "Divide tus sesiones de estudio en bloques de 25 minutos.",
        "Repasa tus notas dentro de las 24 horas posteriores.",
        "Crea mapas mentales para visualizar conexiones.",
        "Practica la recuperación activa poniéndote a prueba frecuentemente.",
        "Usa la repetición espaciada para la retención a largo plazo.",
        "Estudia en un ambiente tranquilo y bien iluminado para mejorar la concentración.",
        "Bebe agua y mantente hidratado para mantener tu mente activa.",
        "Organiza tus materiales de estudio antes de comenzar.",
        "Establece metas específicas para cada sesión de estudio.",
        "Evita la multitarea para maximizar la eficiencia."
    ],
    'fr': [
        "Divisez vos sessions d'étude en blocs de 25 minutes.",
        "Révisez vos notes dans les 24 heures.",
        "Créez des cartes mentales pour visualiser les connexions.",
        "Pratiquez le rappel actif en vous testant fréquemment.",
        "Utilisez la répétition espacée pour une rétention à long terme.",
        "Étudiez dans un environnement calme et bien éclairé pour améliorer la concentration.",
        "Buvez de l'eau et restez hydraté pour garder votre cerveau en forme.",
        "Organisez vos matériaux d'étude avant de commencer.",
        "Fixez des objectifs spécifiques pour chaque session d'étude.",
        "Évitez le multitâche pour maximiser l'efficacité."
    ]
}

@client.tree.command(name="studytip", description="Get a random study tip")
async def study_tip(
    interaction: discord.Interaction,
    topic: Optional[str] = None,
    language: Optional[str] = 'en'
):
    if language not in STUDY_TIPS:
        await interaction.response.send_message("Unsupported language. Available languages: en, es, fr")
        return

    tip = random.choice(STUDY_TIPS[language])
    if topic:
        await interaction.response.send_message(f"\ud83d\udcda **Study Tip for {topic}:** {tip}")
    else:
        await interaction.response.send_message(f"\ud83d\udcda **Study Tip:** {tip}")


@client.tree.command(name="addflashcard", description="Add a new flashcard")
async def add_flashcard(
    interaction: discord.Interaction,
    topic: str,
    question: str,
    answer: str,
    language: str = 'en'
):
    if topic not in client.flashcards:
        client.flashcards[topic] = []
    
    client.flashcards[topic].append({
        "question": question,
        "answer": answer,
        "language": language,
        "created_at": str(datetime.now()),
        "created_by": str(interaction.user.id)
    })
    
    # Award points for contributing
    client.award_points(interaction.user.id, 5)
    client.save_data()
    
    await interaction.response.send_message(
        f"✅ Added flashcard to topic: {topic}\n+5 points for contributing!"
    )

@client.tree.command(name="editflashcard", description="Edit an existing flashcard")
async def edit_flashcard(
    interaction: discord.Interaction,
    topic: str,
    question: str,
    new_answer: str
):
    if topic in client.flashcards:
        for card in client.flashcards[topic]:
            if card["question"] == question:
                card["answer"] = new_answer
                card["updated_at"] = str(datetime.now())
                client.save_data()
                await interaction.response.send_message("✅ Flashcard updated successfully!")
                return
    await interaction.response.send_message("❌ Flashcard not found!")

@client.tree.command(name="quiz", description="Start a quiz on a specific topic")
async def quiz(
    interaction: discord.Interaction,
    topic: str,
    language: str = 'en'
):
    if topic not in client.flashcards or not client.flashcards[topic]:
        await interaction.response.send_message("No flashcards found for this topic!")
        return

    # Filter cards by language
    cards = [card for card in client.flashcards[topic] if card["language"] == language]
    if not cards:
        await interaction.response.send_message(f"No flashcards found for topic '{topic}' in {language}!")
        return

    card = random.choice(cards)
    
    await interaction.response.send_message(
        f"**Topic:** {topic}\n**Question:** {card['question']}\n\n"
        "The answer will be revealed in 10 seconds..."
    )
    
    await asyncio.sleep(10)
    await interaction.followup.send(f"**Answer:** {card['answer']}")
    
    # Update user progress
    user_id = str(interaction.user.id)
    if user_id not in client.user_progress:
        client.user_progress[user_id] = {'points': 0, 'correct_answers': 0, 'total_answers': 0}
    
    client.user_progress[user_id]['total_answers'] += 1
    client.save_data()

@client.tree.command(name="progress", description="Check your study progress")
async def check_progress(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id not in client.user_progress:
        await interaction.response.send_message("No progress recorded yet!")
        return
    
    progress = client.user_progress[user_id]
    accuracy = (progress['correct_answers'] / progress['total_answers'] * 100) if progress['total_answers'] > 0 else 0
    
    embed = discord.Embed(title="Study Progress", color=discord.Color.blue())
    embed.add_field(name="Points", value=progress['points'])
    embed.add_field(name="Total Questions Attempted", value=progress['total_answers'])
    embed.add_field(name="Accuracy", value=f"{accuracy:.1f}%")
    
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="leaderboard", description="Show top performers")
async def show_leaderboard(interaction: discord.Interaction):
    # Sort users by points
    sorted_users = sorted(
        client.user_progress.items(),
        key=lambda x: x[1]['points'],
        reverse=True
    )[:10]  # Top 10
    
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
    
    for i, (user_id, data) in enumerate(sorted_users, 1):
        user = await client.fetch_user(int(user_id))
        embed.add_field(
            name=f"{i}. {user.name}",
            value=f"Points: {data['points']}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="setreminder", description="Set a study reminder")
async def set_reminder(
    interaction: discord.Interaction,
    minutes: int,
    topic: Optional[str] = None
):
    if minutes < 1:
        await interaction.response.send_message("⚠️ Please set a reminder for at least 1 minute!")
        return
    
    await interaction.response.send_message(f"⏰ Reminder set for {minutes} minutes!")
    
    await asyncio.sleep(minutes * 60)
    if topic:
        await interaction.followup.send(
            f"⏰ Time to study {topic}! Get back to work, {interaction.user.mention}!"
        )
    else:
        await interaction.followup.send(
            f"⏰ Time to study! Get back to work, {interaction.user.mention}!"
        )

@client.tree.command(name="export", description="Export flashcards")
async def export_flashcards(
    interaction: discord.Interaction,
    format: str = 'json'
):
    if format not in ['json', 'csv']:
        await interaction.response.send_message("Supported formats: json, csv")
        return
    
    filename = f"flashcards_export.{format}"
    
    if format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(client.flashcards, f, ensure_ascii=False, indent=2)
    else:  # CSV
        # Flatten the data structure for CSV
        rows = []
        for topic, cards in client.flashcards.items():
            for card in cards:
                rows.append({
                    'topic': topic,
                    'question': card['question'],
                    'answer': card['answer'],
                    'language': card['language'],
                    'created_at': card['created_at']
                })
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False, encoding='utf-8')
    
    # Send the file
    with open(filename, 'rb') as f:
        file = discord.File(f, filename=filename)
        await interaction.response.send_message(
            "Here are your flashcards:",
            file=file
        )
    
    # Clean up the file
    os.remove(filename)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'Logged in as {client.user} (ID: {client.user.id})')

# Run the bot
if __name__ == "__main__":
    client.run('MTMyMzk5NTIyMDQxMjcyNzM1Ng.GXUD4h.7UsFAEgMG_kiYSF09uja4nEqTNM2gBgNu-AXh0')
