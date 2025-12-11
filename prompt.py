import json

class PromptEngineer:
    def __init__(self, db_sets: dict):
        """
        Initialize with the 'sets' portion of your database.
        db_sets format: {"category_key": {"description": "...", "ids": [...]}}
        """
        self.sets = db_sets

    def _build_menu_string(self) -> str:
        """
        Private helper: Iterates through the DB and creates the menu text
        formatted specifically for the SLM to understand.
        """
        menu_lines = []
        for key, data in self.sets.items():
            # Creates a line like: - "romance_warm": Low stakes, happy endings.
            line = f'- "{key}": {data["description"]}'
            menu_lines.append(line)
        return "\n".join(menu_lines)

    def generate_system_prompt(self) -> str:
        """
        Constructs the final strict prompt to be sent to the SLM.
        """
        menu_context = self._build_menu_string()

        return f"""
        You are a semantic classification engine for a movie recommendation system.
        
        YOUR TASK:
        Map the User's input to the most relevant categories from the AVAILABLE LIST below.
        
        --- AVAILABLE CATEGORIES ---
        {menu_context}
        
        --- RULES ---
        1. Return ONLY a JSON list of strings containing the exact keys from the list above.
        2. If the user input is complex (e.g., "Funny sci-fi"), select up to 3 matching keys.
        3. If the input is nonsense or unrelated to movies, return [].
        4. Do not output any markdown, code blocks, or conversational text. Return ONLY the raw list.
        
        Example Output: ["romance_warm", "comedy_dark"]
        """

    def generate_recommendation_prompt(self) -> str:
        """
        Constructs a prompt for generating direct movie recommendations.
        """
        return """
        You are a semantic classification engine for a movie recommendation system.
        
        YOUR TASK:
        Based on user's input, suggest best movie recommendations based on popular internet searches or sources such as Reddit, Letterboxd, or IMDB.
        """