import json
import pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data/kb/faq.json"
data = json.loads(P.read_text(encoding="utf-8"))

FAQS = [
    {
        "id": "std_testing",
        "topics": ["sexual_health"],
        "q": {
            "en": "How to check if I have an STD or STI?",
            "hi": "मुझे कैसे पता चले कि मुझे STD/STI है?",
            "hinglish": "STD hai ya nahi kaise check kare",
        },
        "a": {
            "en": "STIs (chlamydia, gonorrhoea, HIV, syphilis) often have NO clear symptoms, so the only reliable way to know is testing. Visit a government hospital or STI clinic - testing and treatment are often free and confidential. See a doctor promptly if you have unusual discharge, sores, rash, or burning during urination. Never self-diagnose from symptoms alone.",
            "hi": "STI (क्लैमाइडिया, गोनोरिया, HIV, सिफलिस) में अक्सर कोई स्पष्ट लक्षण नहीं होते, इसलिए पता करने का एकमात्र विश्वसनीय तरीका जाँच है। सरकारी अस्पताल या STI क्लिनिक जाएँ - जाँच और इलाज अक्सर मुफ़्त और गोपनीय होते हैं। असामान्य स्राव, घाव, चकत्ते या पेशाब में जलन हो तो तुरंत डॉक्टर को दिखाएँ। केवल लक्षणों से खुद निदान न करें।",
        },
        "sources": [{"name": "NACO, MoHFW", "tier": 1}, {"name": "WHO STI Guidance", "tier": 1}],
    },
    {
        "id": "hiv_basics",
        "topics": ["sexual_health"],
        "q": {"en": "What is HIV and how is it tested?", "hi": "HIV क्या है और इसकी जाँच कैसे होती है?", "hinglish": "HIV kya hai aur test kaise hota hai"},
        "a": {
            "en": "HIV is a virus that weakens the immune system over time; it is NOT spread by touch, sharing food or mosquito bites - only through unprotected sex, infected blood/needles, or mother-to-child. A simple blood test detects it; government ICTC centres offer free, confidential testing. Early treatment lets people with HIV live long, healthy lives.",
            "hi": "HIV एक वायरस है जो धीरे-धीरे प्रतिरोधक क्षमता कम करता है; यह छूने, खाना साझा करने या मच्छर से नहीं - केवल असुरक्षित यौन संबंध, संक्रमित रक्त/सुई या माँ से बच्चे में फैलता है। साधारण रक्त जाँच से इसका पता चलता है; सरकारी ICTC केंद्रों पर मुफ़्त, गोपनीय जाँच होती है। समय पर इलाज से HIV वाले लोग लंबा, स्वस्थ जीवन जी सकते हैं।",
        },
        "sources": [{"name": "NACO, MoHFW", "tier": 1}, {"name": "WHO HIV", "tier": 1}],
    },
    {
        "id": "safe_sex",
        "topics": ["sexual_health"],
        "q": {"en": "How can I prevent STIs and HIV?", "hi": "STI और HIV से कैसे बचें?", "hinglish": "STI aur HIV se kaise bache"},
        "a": {
            "en": "Use condoms correctly every time, limit partners, and get tested regularly if at risk. Never share needles or razors. If exposed, PEP (post-exposure) medicine taken within 72 hours can prevent HIV - visit a government hospital immediately.",
            "hi": "हर बार कंडोम का सही उपयोग करें, साथी सीमित रखें और जोखिम हो तो नियमित जाँच कराएँ। सुई या रेज़र कभी साझा न करें। संक्रमण हो जाए तो 72 घंटे के भीतर PEP दवा HIV रोक सकती है - तुरंत सरकारी अस्पताल जाएँ।",
        },
        "sources": [{"name": "NACO, MoHFW", "tier": 1}, {"name": "WHO", "tier": 1}],
    },
    {
        "id": "menstrual_hygiene",
        "topics": ["women_health"],
        "q": {"en": "Menstrual hygiene tips", "hi": "मासिक धर्म के दौरान स्वच्छता के उपाय", "hinglish": "periods me safai kaise rakhe"},
        "a": {
            "en": "Change pads/cloths every 4-6 hours, wash hands before and after, and wash reusable cloth with soap and dry in sunlight. Bathing daily is safe during periods. See a doctor for very heavy bleeding, severe pain, or irregular cycles.",
            "hi": "हर 4-6 घंटे में पैड/कपड़ा बदलें, पहले और बाद में हाथ धोएँ, और धुले कपड़े को धूप में सुखाएँ। मासिक धर्म के दौरान रोज़ नहाना सुरक्षित है। बहुत अधिक रक्तस्राव, तेज़ दर्द या अनियमित माहवारी पर डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO Menstrual Health", "tier": 1}],
    },
    {
        "id": "pregnancy_signs",
        "topics": ["women_health", "pregnancy"],
        "q": {"en": "What are early signs of pregnancy?", "hi": "गर्भावस्था के शुरुआती लक्षण क्या हैं?", "hinglish": "pregnancy ke shuruati lakshan"},
        "a": {
            "en": "Missed period, nausea/vomiting, breast tenderness, frequent urination and tiredness. Confirm with a home pregnancy test or a health centre urine/blood test. Start antenatal care early and take iron-folic acid as advised.",
            "hi": "माहवारी का रुकना, जी मिचलाना/उल्टी, स्तनों में भारीपन, बार-बार पेशाब और थकान। घर के टेस्ट या स्वास्थ्य केंद्र की जाँच से पुष्टि करें। जल्दी प्रसव-पूर्व जाँच शुरू करें और सलाह अनुसार आयरन-फोलिक एसिड लें।",
        },
        "sources": [{"name": "WHO Antenatal Care", "tier": 1}],
    },
    {
        "id": "anxiety_management",
        "topics": ["mental_health"],
        "q": {"en": "How to manage anxiety and stress?", "hi": "चिंता और तनाव कैसे कम करें?", "hinglish": "chinta aur tension kaise kam kare"},
        "a": {
            "en": "Deep slow breathing, regular exercise, enough sleep, limiting caffeine, and talking to someone you trust all help. If anxiety is constant, interferes with daily life, or causes panic, consult a doctor. Tele-MANAS (14416) offers free counselling in India.",
            "hi": "धीमी गहरी साँस, नियमित व्यायाम, पर्याप्त नींद, कैफीन कम करना और किसी विश्वसनीय व्यक्ति से बात करना सहायक है। चिंता लगातार बनी रहे, दैनिक जीवन में बाधा डाले या घबराहट हो तो डॉक्टर से मिलें। भारत में टेली-मानस (14416) मुफ़्त परामर्श देता है।",
        },
        "sources": [{"name": "WHO Mental Health", "tier": 1}, {"name": "Tele-MANAS, MoHFW", "tier": 1}],
    },
    {
        "id": "depression_signs",
        "topics": ["mental_health"],
        "q": {"en": "What are signs of depression?", "hi": "अवसाद (डिप्रेशन) के लक्षण क्या हैं?", "hinglish": "depression ke lakshan"},
        "a": {
            "en": "Persistent sadness or emptiness, loss of interest in things once enjoyed, sleep/appetite changes, tiredness, and hopelessness lasting over two weeks. Depression is a treatable illness, not weakness. Talk to a doctor; help is available (Tele-MANAS 14416).",
            "hi": "लगातार उदासी, पसंद की चीज़ों में रुचि कम होना, नींद/भूख में बदलाव, थकान और निराशा जो दो सप्ताह से अधिक रहे। अवसाद इलाज योग्य बीमारी है, कमज़ोरी नहीं। डॉक्टर से बात करें; मदद उपलब्ध है (टेली-मानस 14416)।",
        },
        "sources": [{"name": "WHO Depression", "tier": 1}, {"name": "Tele-MANAS, MoHFW", "tier": 1}],
    },
    {
        "id": "sleep_hygiene",
        "topics": ["mental_health", "lifestyle"],
        "q": {"en": "How to improve sleep?", "hi": "नींद कैसे अच्छी आए?", "hinglish": "neend kaise achi aaye"},
        "a": {
            "en": "Sleep and wake at the same time daily, avoid tea/coffee after evening, keep the room dark and quiet, and avoid mobile screens before bed. Adults need 7-9 hours. See a doctor for persistent insomnia.",
            "hi": "रोज़ एक ही समय पर सोएँ और जागें, शाम के बाद चाय/कॉफी से बचें, कमरा अँधेरा और शांत रखें, सोने से पहले मोबाइल न देखें। वयस्कों को 7-9 घंटे की नींद चाहिए। लगातार अनिद्रा हो तो डॉक्टर से मिलें।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "asthma_basics",
        "topics": ["respiratory"],
        "q": {"en": "What is asthma and how to manage it?", "hi": "अस्थमा (दमा) क्या है और उसे कैसे संभालें?", "hinglish": "asthma kya hai aur kaise control kare"},
        "a": {
            "en": "Asthma is a long-term lung condition causing wheezing, cough and breathlessness, often triggered by dust, smoke, cold air or allergies. It is controlled with inhalers as prescribed - not cured. Avoid smoke and dust, and always carry the prescribed inhaler.",
            "hi": "अस्थमा फेफड़ों की एक पुरानी बीमारी है जिसमें घरघराहट, खाँसी और साँस फूलती है, अक्सर धूल, धुएँ, ठंडी हवा या एलर्जी से। यह डॉक्टर द्वारा बताए इनहेलर से नियंत्रित होती है - पूरी तरह ठीक नहीं होती। धुएँ-धूल से बचें और इनहेलर हमेशा साथ रखें।",
        },
        "sources": [{"name": "WHO Asthma", "tier": 1}],
    },
    {
        "id": "allergy_basics",
        "topics": ["respiratory"],
        "q": {"en": "Common allergy symptoms and how to manage them", "hi": "एलर्जी के लक्षण और उनका प्रबंधन", "hinglish": "allergy ke lakshan aur ilaaj"},
        "a": {
            "en": "Sneezing, runny/itchy nose, watery eyes, and skin rashes are common. Avoid the trigger (dust, pollen, certain foods), keep the house dust-free, and take antihistamines as a doctor advises. Severe swelling or breathing trouble is an emergency - get help immediately.",
            "hi": "छींक, नाक बहना/खुजली, आँखों से पानी और त्वचा पर चकत्ते आम हैं। कारण (धूल, पराग, कुछ खाने) से बचें, घर को धूल-रहित रखें, और डॉक्टर की सलाह से एंटीहिस्टामिन लें। गंभीर सूजन या साँस लेने में तकलीफ आपातकाल है - तुरंत मदद लें।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "acidity_gerd",
        "topics": ["digestive"],
        "q": {"en": "How to relieve acidity and heartburn?", "hi": "एसिडिटी और सीने में जलन से कैसे राहत पाएँ?", "hinglish": "acidity aur gale me jalan ka ilaaj"},
        "a": {
            "en": "Eat smaller meals, avoid spicy/oily food, don't lie down right after eating, and avoid alcohol and smoking. Persistent or severe heartburn, difficulty swallowing, or weight loss needs a doctor.",
            "hi": "थोड़ा-थोड़ा खाएँ, मसालेदार/तला भोजन से बचें, खाने के तुरंत बाद न लेटें, और शराब व धूम्रपान से बचें। लगातार या तेज़ जलन, निगलने में कठिनाई या वज़न घटना हो तो डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "constipation_relief",
        "topics": ["digestive"],
        "q": {"en": "How to relieve constipation?", "hi": "कब्ज़ से कैसे राहत पाएँ?", "hinglish": "kabz ka ilaaj"},
        "a": {
            "en": "Drink plenty of water, eat fibre-rich food (vegetables, fruits, whole grains), stay active, and don't ignore the urge to go. Laxatives should only be used on a doctor's advice. See a doctor for blood in stool or long-lasting constipation.",
            "hi": "खूब पानी पिएँ, रेशेदार भोजन (सब्ज़ियाँ, फल, साबुत अनाज) खाएँ, सक्रिय रहें और शौच की इच्छा को न रोकें। जुलाब केवल डॉक्टर की सलाह पर लें। मल में खून या लंबे समय की कब्ज़ पर डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "food_poisoning",
        "topics": ["digestive"],
        "q": {"en": "Food poisoning symptoms and care", "hi": "फूड पॉइज़निंग के लक्षण और देखभाल", "hinglish": "food poisoning ke lakshan"},
        "a": {
            "en": "Vomiting, diarrhoea, stomach cramps and sometimes fever, usually starting hours after eating contaminated food. Drink ORS/fluids, rest, and avoid solid food briefly. Seek care for blood in stool, high fever, or signs of dehydration.",
            "hi": "उल्टी, दस्त, पेट में मरोड़ और कभी-कभी बुखार, आमतौर पर दूषित भोजन खाने के कुछ घंटों बाद शुरू होते हैं। ORS/तरल पदार्थ लें, आराम करें और कुछ देर ठोस भोजन न खाएँ। मल में खून, तेज़ बुखार या पानी की कमी पर चिकित्सा सहायता लें।",
        },
        "sources": [{"name": "WHO Food Safety", "tier": 1}],
    },
    {
        "id": "conjunctivitis",
        "topics": ["eye"],
        "q": {"en": "Conjunctivitis (eye infection) care", "hi": "आँख आना (कंजंक्टिवाइटिस) की देखभाल", "hinglish": "aankh aana ka ilaaj"},
        "a": {
            "en": "Red, itchy, watery eyes with discharge - often viral and self-limiting. Wash hands often, don't rub or share towels, and clean discharge with clean cloth. See a doctor for pain, blurred vision or if it doesn't improve in a few days.",
            "hi": "लाल, खुजलीदार, पानी वाली आँखें और कीचड़ - अक्सर वायरल और अपने आप ठीक हो जाता है। बार-बार हाथ धोएँ, आँखें न मलें, तौलिया साझा न करें और साफ़ कपड़े से कीचड़ हटाएँ। दर्द, धुंधला दिखना या कुछ दिनों में आराम न मिलने पर डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "ear_infection",
        "topics": ["child_health", "ent"],
        "q": {"en": "Ear pain and infection in children", "hi": "बच्चों में कान दर्द और संक्रमण", "hinglish": "bache ke kaan me dard"},
        "a": {
            "en": "Ear pain, fever, irritability and pulling at the ear in young children. Avoid putting oil/drops without a doctor's advice, keep the child comfortable with paracetamol as advised, and see a doctor for proper diagnosis.",
            "hi": "कान में दर्द, बुखार, चिड़चिड़ापन और छोटे बच्चों का कान खींचना। डॉक्टर की सलाह के बिना तेल/ड्रॉप न डालें, सलाह अनुसार पैरासिटामोल से आराम दें और सही निदान के लिए डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "fungal_skin",
        "topics": ["skin"],
        "q": {"en": "Ringworm and fungal skin infections", "hi": "दाद और फंगल त्वचा संक्रमण", "hinglish": "daad khujli ka ilaaj"},
        "a": {
            "en": "Itchy red ring-shaped patches, common in warm sweaty folds. Keep skin clean and dry, wear loose cotton clothes, don't share towels, and complete the full antifungal cream/medicine course as prescribed. See a doctor for spreading or persistent infection.",
            "hi": "खुजलीदार लाल गोल चकत्ते, गर्म पसीने वाले हिस्सों में आम। त्वचा साफ़-सूखी रखें, ढीले सूती कपड़े पहनें, तौलिया साझा न करें और डॉक्टर द्वारा बताई फंगल क्रीम/दवा का पूरा कोर्स पूरा करें। फैलता या लगातार संक्रमण हो तो डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "scabies",
        "topics": ["skin"],
        "q": {"en": "Scabies and intense itching", "hi": "खुजली (स्केबीज़) का इलाज", "hinglish": "khujli scabies ka ilaaj"},
        "a": {
            "en": "Scabies causes intense night-time itching and a rash from tiny mites, spreading by close contact. It needs a prescribed scabicide lotion applied to the whole body, and all family members should be treated together. Wash clothes/bedding in hot water.",
            "hi": "स्केबीज़ में रात में तेज़ खुजली और छोटे कीट से चकत्ते होते हैं, यह निकट संपर्क से फैलता है। डॉक्टर द्वारा बताया स्केबीसाइड लोशन पूरे शरीर पर लगाना ज़रूरी है, और परिवार के सभी सदस्यों का एक साथ इलाज होना चाहिए। कपड़े/बिस्तर गर्म पानी में धोएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "back_pain",
        "topics": ["bone_joint"],
        "q": {"en": "Lower back pain management", "hi": "कमर दर्द का प्रबंधन", "hinglish": "kamar dard ka ilaaj"},
        "a": {
            "en": "Most back pain improves with staying gently active, avoiding long bed rest, and heat. Improve posture and lift properly. See a doctor for pain radiating down the leg, numbness, weakness, or loss of bladder/bowel control.",
            "hi": "अधिकांश कमर दर्द हल्की सक्रियता, लंबे बिस्तर-आराम से बचने और सेंक से ठीक होता है। मुद्रा सुधारें और सही तरीके से वज़न उठाएँ। दर्द पैर में जाए, सुन्नता, कमज़ोरी या पेशाब/मल पर नियंत्रण न रहे तो तुरंत डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
    {
        "id": "sprain_rice",
        "topics": ["bone_joint", "first_aid"],
        "q": {"en": "What to do for a sprain or muscle injury?", "hi": "मोच या मांसपेशी की चोट पर क्या करें?", "hinglish": "moch aane par kya kare"},
        "a": {
            "en": "Follow RICE: Rest the injured part, apply Ice (wrapped in cloth) for 15-20 min, Compress gently with a bandage, and Elevate the limb. Avoid heat or massage in the first 48 hours. See a doctor if pain is severe or you cannot bear weight.",
            "hi": "RICE नियम अपनाएँ: चोट वाले हिस्से को आराम (Rest), कपड़े में लपेटकर 15-20 मिनट बर्फ (Ice), हल्की पट्टी (Compress), और अंग ऊपर रखें (Elevate)। पहले 48 घंटे सेंक या मालिश न करें। तेज़ दर्द हो या वज़न सहन न हो तो डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO First Aid", "tier": 1}],
    },
    {
        "id": "cholesterol",
        "topics": ["lifestyle"],
        "q": {"en": "High cholesterol and diet", "hi": "उच्च कोलेस्ट्रॉल और आहार", "hinglish": "cholesterol kaise kam kare"},
        "a": {
            "en": "Reduce fried and fatty food, use less oil/ghee, eat more fruits, vegetables and whole grains, and exercise regularly. Get a lipid profile test if you have diabetes, high BP, or a family history. Medicines are prescribed by a doctor when needed.",
            "hi": "तला-भुना और चिकनाई कम करें, तेल/घी कम लें, अधिक फल-सब्ज़ियाँ और साबुत अनाज खाएँ, नियमित व्यायाम करें। मधुमेह, उच्च रक्तचाप या पारिवारिक इतिहास हो तो लिपिड प्रोफाइल जाँच कराएँ। ज़रूरत पड़ने पर दवा डॉक्टर देते हैं।",
        },
        "sources": [{"name": "WHO", "tier": 1}],
    },
]

existing = {f["id"] for f in data["faqs"]}
added = 0
for f in FAQS:
    if f["id"] in existing:
        continue
    data["faqs"].append(f)
    added += 1

P.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"added {added} FAQs; total now {len(data['faqs'])}")
