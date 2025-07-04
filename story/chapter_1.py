"""
Capítulo 1: Bienvenida a la Mansión Diana
Sistema narrativo interactivo
"""

class Chapter1:
    """Primer capítulo de la historia de Diana"""
    
    def __init__(self):
        self.chapter_id = "chapter_1"
        self.title = "Bienvenida a la Mansión"
        self.scenes = {
            "entrance": self._scene_entrance,
            "hall": self._scene_main_hall,
            "library": self._scene_library,
            "garden": self._scene_garden,
            "diana_meeting": self._scene_diana_meeting
        }
        
    def get_scene(self, scene_id: str, user_data: dict = None):
        """Obtiene una escena específica del capítulo"""
        if scene_id in self.scenes:
            return self.scenes[scene_id](user_data or {})
        return self._scene_not_found()
    
    def _scene_entrance(self, user_data: dict):
        """Escena de entrada a la mansión"""
        user_name = user_data.get('name', 'invitado')
        
        return {
            "scene_id": "entrance",
            "title": "🏰 La Entrada",
            "text": (
                f"🎩 **Lucien te recibe en la entrada**\n\n"
                f"*Las enormes puertas de roble se abren lentamente ante ti, {user_name}. "
                f"El eco de tus pasos resuena en el vestíbulo de mármol mientras Lucien, "
                f"impecablemente vestido, se inclina en una reverencia.*\n\n"
                f"**Lucien:** \"Bienvenido a la Mansión Diana, {user_name}. "
                f"Lady Diana 👑 ha estado esperando su llegada con gran expectación.\"\n\n"
                f"*El aire está impregnado de un sutil aroma a jazmín y misterio...*"
            ),
            "choices": [
                {
                    "text": "🚪 Seguir a Lucien al salón principal",
                    "action": "goto_scene",
                    "target": "hall",
                    "besitos_reward": 25
                },
                {
                    "text": "👀 Observar los detalles del vestíbulo",
                    "action": "explore",
                    "target": "entrance_details",
                    "besitos_reward": 15
                },
                {
                    "text": "💬 Preguntar sobre Lady Diana",
                    "action": "dialogue",
                    "target": "diana_info",
                    "besitos_reward": 20
                }
            ],
            "background_music": "mansion_entrance.mp3",
            "completion_reward": 50
        }
    
    def _scene_main_hall(self, user_data: dict):
        """Escena del salón principal"""
        return {
            "scene_id": "hall",
            "title": "🏛️ El Gran Salón",
            "text": (
                f"🎩 **El corazón de la mansión**\n\n"
                f"*Lucien te guía a través de un majestuoso salón. Candelabros de cristal "
                f"cuelgan del techo abovedado, proyectando destellos dorados sobre "
                f"los retratos ancestrales que adornan las paredes.*\n\n"
                f"**Lucien:** \"Este es el corazón de nuestra mansión. Desde aquí, "
                f"puede acceder a la biblioteca 📚, los jardines 🌹, o... "
                f"si se siente preparado, a los aposentos privados de Lady Diana 👑.\"\n\n"
                f"*Una suave melodía de piano flota desde algún lugar distante...*"
            ),
            "choices": [
                {
                    "text": "📚 Explorar la biblioteca",
                    "action": "goto_scene",
                    "target": "library",
                    "besitos_reward": 30
                },
                {
                    "text": "🌹 Pasear por los jardines",
                    "action": "goto_scene", 
                    "target": "garden",
                    "besitos_reward": 35
                },
                {
                    "text": "👑 Solicitar audiencia con Lady Diana",
                    "action": "goto_scene",
                    "target": "diana_meeting",
                    "besitos_reward": 100,
                    "requirement": {"level": 3}
                }
            ],
            "completion_reward": 75
        }
    
    def _scene_library(self, user_data: dict):
        """Escena de la biblioteca"""
        return {
            "scene_id": "library",
            "title": "📚 La Biblioteca Secreta",
            "text": (
                f"📖 **Conocimiento y misterios**\n\n"
                f"*La biblioteca se extiende en múltiples niveles, con estanterías "
                f"que parecen tocar el cielo. Libros antiguos y pergaminos "
                f"descansan en perfecta armonía.*\n\n"
                f"**Lucien:** \"Lady Diana 👑 es una ávida coleccionista de conocimiento. "
                f"Aquí encontrará historias que pocos mortales han leído...\"\n\n"
                f"*Notas un libro que brilla suavemente en un estante alto...*"
            ),
            "choices": [
                {
                    "text": "✨ Tomar el libro brillante",
                    "action": "special_item",
                    "target": "mystical_book",
                    "besitos_reward": 150
                },
                {
                    "text": "📜 Leer pergaminos antiguos",
                    "action": "lore",
                    "target": "ancient_lore",
                    "besitos_reward": 75
                },
                {
                    "text": "🔍 Buscar pistas sobre Diana",
                    "action": "investigation",
                    "target": "diana_clues",
                    "besitos_reward": 100
                }
            ],
            "completion_reward": 125
        }
    
    def _scene_garden(self, user_data: dict):
        """Escena de los jardines"""
        return {
            "scene_id": "garden",
            "title": "🌹 Los Jardines Encantados",
            "text": (
                f"🌸 **Belleza natural y magia**\n\n"
                f"*Los jardines se extienden como un tapiz viviente. Rosas rojas "
                f"y blancas danzan al viento, mientras fuentes de mármol "
                f"susurran melodías acuáticas.*\n\n"
                f"**Lucien:** \"Lady Diana 👑 pasa muchas tardes aquí. "
                f"Dice que las flores le susurran secretos...\"\n\n"
                f"*Una mariposa dorada se posa en tu hombro...*"
            ),
            "choices": [
                {
                    "text": "🦋 Seguir a la mariposa dorada",
                    "action": "magical_encounter",
                    "target": "golden_butterfly",
                    "besitos_reward": 200
                },
                {
                    "text": "🌹 Recoger una rosa especial",
                    "action": "collect_item",
                    "target": "diana_rose",
                    "besitos_reward": 125
                },
                {
                    "text": "⛲ Hacer un deseo en la fuente",
                    "action": "wish",
                    "target": "fountain_wish",
                    "besitos_reward": 75
                }
            ],
            "completion_reward": 150
        }
    
    def _scene_diana_meeting(self, user_data: dict):
        """Escena del encuentro con Diana"""
        user_name = user_data.get('name', 'querido invitado')
        
        return {
            "scene_id": "diana_meeting",
            "title": "👑 Audiencia con Lady Diana",
            "text": (
                f"👑 **El encuentro esperado**\n\n"
                f"*Las puertas dobles se abren revelando un salón íntimo bañado "
                f"en luz dorada. Lady Diana, de belleza etérea, se encuentra "
                f"junto a una ventana contemplando los jardines.*\n\n"
                f"**Diana:** \"Ah, {user_name}... Lucien me ha hablado mucho de ti. "
                f"Tu dedicación no ha pasado desapercibida...\"\n\n"
                f"*Sus ojos parecen contener galaxias enteras...*\n\n"
                f"**Diana:** \"Dime, ¿qué es lo que realmente buscas en mi mansión?\""
            ),
            "choices": [
                {
                    "text": "💋 'Busco conocerte mejor, Lady Diana'",
                    "action": "romance_path",
                    "target": "romance_route",
                    "besitos_reward": 500
                },
                {
                    "text": "🎯 'Busco aventuras y desafíos'",
                    "action": "adventure_path",
                    "target": "adventure_route",
                    "besitos_reward": 300
                },
                {
                    "text": "🧠 'Busco conocimiento y sabiduría'",
                    "action": "wisdom_path",
                    "target": "wisdom_route",
                    "besitos_reward": 400
                }
            ],
            "completion_reward": 1000,
            "unlocks": ["chapter_2", "diana_private_missions"]
        }
    
    def _scene_not_found(self):
        """Escena por defecto cuando no se encuentra la solicitada"""
        return {
            "scene_id": "not_found",
            "title": "❓ Escena no encontrada",
            "text": "🎩 **Lucien:** \"Disculpe, parece que se ha perdido. Permítame guiarlo de vuelta.\"",
            "choices": [
                {
                    "text": "🏠 Volver al salón principal",
                    "action": "goto_scene",
                    "target": "hall",
                    "besitos_reward": 0
                }
            ],
            "completion_reward": 0
        }

class StoryManager:
    """Gestor principal del sistema narrativo"""
    
    def __init__(self):
        self.chapters = {
            "chapter_1": Chapter1()
        }
        
    def get_chapter(self, chapter_id: str):
        """Obtiene un capítulo específico"""
        return self.chapters.get(chapter_id)
    
    def get_scene(self, chapter_id: str, scene_id: str, user_data: dict = None):
        """Obtiene una escena específica de un capítulo"""
        chapter = self.get_chapter(chapter_id)
        if chapter:
            return chapter.get_scene(scene_id, user_data)
        return None
    
    def get_available_chapters(self, user_level: int):
        """Obtiene capítulos disponibles según el nivel del usuario"""
        available = []
        
        # Capítulo 1 siempre disponible
        if user_level >= 1:
            available.append("chapter_1")
            
        # Futuros capítulos según nivel
        if user_level >= 5:
            available.append("chapter_2")
        if user_level >= 10:
            available.append("chapter_3")
            
        return available
