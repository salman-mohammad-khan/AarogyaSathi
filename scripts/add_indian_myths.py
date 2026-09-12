import json
import pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "data/kb/myths.json"
data = json.loads(P.read_text(encoding="utf-8"))

new_myths = [
    {
        "id": "kadha_immunity",
        "claim": {"en": "Drinking homemade kadha (herbal decoction) boosts immunity and prevents diseases.", "hi": "घर का बना काढ़ा पीने से रोग प्रतिरोधक क्षमता बढ़ती है और बीमारियाँ नहीं होतीं।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "immunity"],
        "fear_mongering": False,
        "explanation": {
            "en": "Kadha (ginger, tulsi, honey) is a warm, soothing drink that may ease cold and cough symptoms. But there is no strong scientific proof it 'boosts immunity' to prevent diseases - immunity is not switched on by one drink. It is a supportive wellness drink, not a disease shield or a medicine.",
            "hi": "काढ़ा (अदरक, तुलसी, शहद) एक गर्म, आरामदायक पेय है जो सर्दी-खाँसी के लक्षणों में राहत दे सकता है। पर इसका कोई पुख्ता वैज्ञानिक प्रमाण नहीं कि यह बीमारियों से बचाने के लिए 'रोग प्रतिरोधक क्षमता बढ़ा देता है'। यह सहायक पेय है, बीमारी से बचाने वाली ढाल या दवा नहीं।"
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}, {"name": "Limited clinical evidence", "tier": 2}]
    },
    {
        "id": "giloy_dengue",
        "claim": {"en": "Giloy (Tinospora cordifolia) cures dengue fever.", "hi": "गिलोय डेंगू बुखार ठीक कर देता है।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "dengue"],
        "fear_mongering": False,
        "explanation": {
            "en": "Some preliminary studies suggest giloy may support immunity and platelet recovery, but it is NOT a proven cure for dengue. Dengue has no specific cure - treatment is rest, fluids and medical monitoring. Do not rely on giloy instead of seeing a doctor.",
            "hi": "कुछ शुरुआती अध्ययन बताते हैं कि गिलोय रोग प्रतिरोधक क्षमता और प्लेटलेट सुधार में सहायक हो सकता है, पर यह डेंगू का सिद्ध इलाज नहीं है। डेंगू का कोई विशेष इलाज नहीं - आराम, तरल पदार्थ और चिकित्सकीय निगरानी ही उपचार है। डॉक्टर को दिखाने की जगह गिलोय पर निर्भर न रहें।"
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}, {"name": "Limited clinical evidence", "tier": 2}]
    },
    {
        "id": "tulsi_fever",
        "claim": {"en": "Tulsi (holy basil) leaves cure all fevers.", "hi": "तुलसी के पत्ते हर तरह का बुखार ठीक कर देते हैं।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "fever"],
        "fear_mongering": False,
        "explanation": {
            "en": "Tulsi has some antimicrobial properties and is used traditionally. It may soothe, but it does not cure all fevers. Fever can have many causes (dengue, typhoid, malaria) that need proper diagnosis. Persistent or high fever needs a doctor.",
            "hi": "तुलसी में कुछ रोगाणुरोधी गुण होते हैं और इसे पारंपरिक रूप से इस्तेमाल किया जाता है। यह आराम दे सकती है, पर हर तरह का बुखार ठीक नहीं करती। बुखार के कई कारण हो सकते हैं (डेंगू, टाइफाइड, मलेरिया) जिनका सही निदान ज़रूरी है। लगातार या तेज़ बुखार पर डॉक्टर को दिखाएँ।"
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}]
    },
    {
        "id": "haldi_doodh_cold",
        "claim": {"en": "Haldi doodh (turmeric milk) cures cold and cough.", "hi": "हल्दी वाला दूध सर्दी-खाँसी ठीक कर देता है।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "cold"],
        "fear_mongering": False,
        "explanation": {
            "en": "Turmeric contains curcumin which has anti-inflammatory properties, and warm milk is soothing. But haldi doodh is not a proven cure for the viral infections that cause cold and cough. It gives comfort, not a cure.",
            "hi": "हल्दी में करक्यूमिन होता है जिसमें सूजन-रोधी गुण हैं, और गर्म दूध आराम देता है। पर हल्दी वाला दूध सर्दी-खाँसी पैदा करने वाले वायरल संक्रमण का सिद्ध इलाज नहीं है। यह आराम देता है, इलाज नहीं।"
        },
        "sources": [{"name": "NIH (curcumin studies)", "tier": 2}]
    },
    {
        "id": "chyawanprash_immunity",
        "claim": {"en": "Chyawanprash boosts immunity and prevents all diseases.", "hi": "च्यवनप्राश रोग प्रतिरोधक क्षमता बढ़ाता है और सभी बीमारियों से बचाता है।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "immunity"],
        "fear_mongering": False,
        "explanation": {
            "en": "Chyawanprash is a traditional Ayurvedic preparation rich in vitamins and antioxidants that may support general health. There is no proof it prevents all diseases. A balanced diet, sleep and exercise matter far more.",
            "hi": "च्यवनप्राश विटामिन और एंटीऑक्सीडेंट से भरपूर पारंपरिक आयुर्वेदिक तैयारी है जो सामान्य स्वास्थ्य में सहायक हो सकती है। इसका कोई प्रमाण नहीं कि यह सभी बीमारियों से बचाता है। संतुलित आहार, नींद और व्यायाम कहीं अधिक महत्वपूर्ण हैं।"
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}]
    },
    {
        "id": "neem_chickenpox",
        "claim": {"en": "Applying neem leaves cures chickenpox.", "hi": "नीम की पत्तियाँ लगाने से चेचक ठीक हो जाती है।"},
        "verdict": "MYTH",
        "tags": ["home_remedy", "chickenpox"],
        "fear_mongering": False,
        "explanation": {
            "en": "Neem paste may soothe the itching of chickenpox, but it does not cure the viral infection. The body clears it on its own; keep the child hydrated and see a doctor for high fever or complications.",
            "hi": "नीम का लेप चेचक की खुजली में आराम दे सकता है, पर यह वायरल संक्रमण को ठीक नहीं करता। शरीर इसे स्वयं ठीक करता है; बच्चे को हाइड्रेट रखें और तेज़ बुखार या जटिलता पर डॉक्टर को दिखाएँ।"
        },
        "sources": [{"name": "WHO", "tier": 1}]
    },
    {
        "id": "jeera_water_weight",
        "claim": {"en": "Jeera (cumin) water helps digestion and reduces weight.", "hi": "जीरे का पानी पाचन में मदद करता है और वज़न घटाता है।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "nutrition"],
        "fear_mongering": False,
        "explanation": {
            "en": "Jeera water is a traditional digestive aid and can help with mild bloating. But the weight-loss claim has weak scientific evidence - no single drink causes meaningful weight loss without diet and exercise.",
            "hi": "जीरे का पानी पाचन का पारंपरिक सहायक है और हल्की अपच में मदद कर सकता है। पर वज़न घटाने का दावा कमज़ोर वैज्ञानिक प्रमाण पर है - बिना आहार और व्यायाम के कोई एक पेय वज़न नहीं घटाता।"
        },
        "sources": [{"name": "Limited clinical evidence", "tier": 2}]
    },
    {
        "id": "lemon_honey_cold",
        "claim": {"en": "Lemon and honey in warm water cures cold and cough.", "hi": "नींबू और शहद का गर्म पानी सर्दी-खाँसी ठीक कर देता है।"},
        "verdict": "PARTLY_TRUE",
        "tags": ["home_remedy", "cold"],
        "fear_mongering": False,
        "explanation": {
            "en": "Lemon provides vitamin C and honey soothes the throat, so this drink can ease symptoms. But it does not cure the viral infection causing the cold. It is supportive, not a cure.",
            "hi": "नींबू विटामिन C देता है और शहद गले को आराम देता है, इसलिए यह पेय लक्षणों में राहत दे सकता है। पर यह सर्दी पैदा करने वाले वायरल संक्रमण को ठीक नहीं करता। यह सहायक है, इलाज नहीं।"
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}]
    },
    {
        "id": "ghee_arthritis",
        "claim": {"en": "Applying ghee or oil on joints cures arthritis.", "hi": "जोड़ों पर घी या तेल लगाने से गठिया (आर्थराइटिस) ठीक हो जाता है।"},
        "verdict": "MYTH",
        "tags": ["home_remedy", "arthritis"],
        "fear_mongering": False,
        "explanation": {
            "en": "There is no evidence that applying ghee or oil cures arthritis. Gentle massage may give temporary comfort, but arthritis needs proper medical management. Relying on massage alone delays effective treatment.",
            "hi": "इसका कोई प्रमाण नहीं कि घी या तेल लगाने से गठिया ठीक होता है। हल्की मालिश से अस्थायी आराम मिल सकता है, पर गठिया का सही चिकित्सकीय प्रबंधन ज़रूरी है। केवल मालिश पर निर्भर रहने से सही इलाज में देरी होती है।"
        },
        "sources": [{"name": "NIH (arthritis)", "tier": 2}]
    },
    {
        "id": "saunf_digestion",
        "claim": {"en": "Eating saunf (fennel seeds) after meals improves digestion.", "hi": "खाने के बाद सौंफ खाने से पाचन अच्छा होता है।"},
        "verdict": "TRUE",
        "tags": ["nutrition"],
        "fear_mongering": False,
        "explanation": {
            "en": "Fennel seeds are a traditional, safe digestive aid commonly eaten after meals in India. This is a harmless, widely accepted practice with no downside for most people.",
            "hi": "सौंफ पाचन का पारंपरिक और सुरक्षित सहायक है, जिसे भारत में आमतौर पर खाने के बाद खाया जाता है। अधिकांश लोगों के लिए यह हानिरहित और स्वीकृत आदत है।"
        },
        "sources": [{"name": "Traditional practice", "tier": 2}]
    },
]

existing_ids = {m["id"] for m in data["myths"]}
added = 0
for m in new_myths:
    if m["id"] in existing_ids:
        continue
    data["myths"].append(m)
    added += 1

P.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"added {added} myths; total now {len(data['myths'])}")
