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
        You are a movie recommendation engine.
        
        YOUR TASK:
        Based on the user's input, suggest 3-5 movie recommendations.
        
        --- RESPONSE FORMAT ---
        You MUST return a valid JSON object with the following structure:
        {
            "user_input": "The original input text",
            "recommendations": [
                {
                    "title": "Movie Title",
                    "director": "Director Name",
                    "writer": "Writer Name",
                    "cast": "Key Cast Members",
                    "quote": "A memorable quote from the movie",
                    "trigger_warning": "Any trigger warnings (or empty string if none)",
                    "poster_details": "A visual description of the poster"
                }
            ]
        }
        
        --- RULES ---
        1. Return ONLY the JSON object. Do not add any markdown formatting (like ```json), commentary, or extra text.
        2. Ensure the JSON is valid and can be parsed.
        3. 'trigger_warning' can be an empty string if there are no significant warnings.
        4. 'poster_details' should be a visual description of the poster.
        5. GIBBERISH HANDLING: If the user input is gibberish, nonsense, or random characters (e.g. "asdf", "gfhj", "blah"):
           - Return a JSON with the specific note: "just like your query, we don’t understand these movies."
           - Return 3 "mind-bending" movie recommendations (e.g. Inception, Primer, Coherence, Tenet).
           - Do NOT try to interpret the gibberish.
        """