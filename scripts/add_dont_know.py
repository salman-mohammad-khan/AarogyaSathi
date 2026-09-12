import json
import pathlib

p = pathlib.Path("data/kb/messages.json")
data = json.loads(p.read_text(encoding="utf-8"))
data["en"]["dont_know"] = (
    "I'm sorry, I don't have reliable health information about that. I'm a health assistant - "
    "ask me about symptoms, diseases, prevention, vaccines, or health messages (e.g. 'fact check: ...')."
)
data["hi"]["dont_know"] = (
    "क्षमा करें, मेरे पास इसके बारे में विश्वसनीय स्वास्थ्य जानकारी नहीं है। मैं एक स्वास्थ्य सहायक हूँ - "
    "लक्षणों, बीमारियों, बचाव, टीकों या स्वास्थ्य संदेशों के बारे में पूछें (जैसे 'fact check: ...')।"
)
p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("dont_know added to messages.json")