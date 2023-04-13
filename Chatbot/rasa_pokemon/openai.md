# OpenAI API (ChatGPT) in Rasa Chatbot einbinden

Um das OpenAI API in einen Rasa Chatbot einzubauen, müssen Sie zuerst eine Verbindung zwischen Ihrem Rasa-Projekt und dem OpenAI-API herstellen. Hier sind die Schritte, wie Sie dies tun können:

1. Installieren Sie die OpenAI-Bibliothek:

```bash
pip install openai
```

2. Erstellen Sie eine neue Datei namens `openai_actions.py` in Ihrem Rasa-Projektverzeichnis:

```python
from typing import Any, Text, Dict, List
import openai
import os

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

openai.api_key = os.environ["OPENAI_API_KEY"]

class ActionGetOpenAIResponse(Action):
    def name(self) -> Text:
        return "action_get_openai_response"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        message = tracker.latest_message.get("text")

        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=message,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5
        )

        reply = response.choices[0].text.strip()
        dispatcher.utter_message(text=reply)

        return []
```

3. Aktualisieren Sie Ihre `config.yml` Datei, um die benutzerdefinierte Aktion zu verwenden:

```yaml
actions:
  - action_get_openai_response
```

4. Aktualisieren Sie Ihre `domain.yml`, um die benutzerdefinierte Aktion zu enthalten:

```yaml
actions:
  - action_get_openai_response
```

5. Aktualisieren Sie Ihre `rules.yml` oder `stories.yml`, um die benutzerdefinierte Aktion zu verwenden:

```yaml
- rule: Get OpenAI response
  steps:
  - intent: get_response
  - action: action_get_openai_response
```

6. Setzen Sie Ihre OpenAI-API-Key in Ihre Umgebungsvariablen oder fügen Sie sie direkt in `openai_actions.py`:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

7. Starten Sie den Rasa-Server und den Aktions-Server:

```bash
rasa run actions
rasa run
```

Jetzt sollte Ihr Rasa-Chatbot in der Lage sein, OpenAI API für die Generierung von Antworten zu verwenden. Achten Sie darauf, die API-Anfragen zu optimieren und Limits zu beachten, um die Kosten im Rahmen zu halten.
