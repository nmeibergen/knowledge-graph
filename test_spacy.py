# Before being able to load the dutch nlp package run:
# > pipenv shell
# > python3 -m spacy download nl_core_news_sm

import pandas as pd
import spacy
import textacy

from spacy import displacy
nlp = spacy.load('nl_core_news_sm')
#nlp = spacy.load('en_core_web_sm')

df_docs = pd.DataFrame({'content': ["Hoe is het om bij Sherpa te wonen en te werken? Aan de hand van dit vraagstuk bezocht Beau de zorginstelling aan de Zandheuvelweg in Baarn. Hij maakt in de docuserie 'Beau Five Days Inside' kennis met een aantal bewoners, locaties en het werk van de begeleiders. Sherpa benadrukt dat het een mooie mogelijkheid is om de gehandicaptenzorg landelijk onder de aandacht te brengen. 'Wij zijn ontzettend trots op het prachtige resultaat. '. Uitzending gemist. ‘Beau Five Days Inside’ werd op dinsdag 27 februari 2018 uitgezonden en kun je hier terugkijken met een Videoland abonnement. Communicatie. Hieronder staan een aantal middelen die je kunt inzetten om de communicatie met mensen met een verstandelijke beperking én of ernstig meervoudige beperking te ondersteunen: Studiemateriaal Disability Studies. Tovertafel, LACCS, CRDL, Snoezelkamer. Imiteren. Meer informatie: Cliëntgroep ernstig meervoudige beperking. Cliëntgroep verstandelijke beperking. Kwaliteitsrapport: 'Oog voor dialoog, aandacht voor elkaar'.",
                                    "Drie aanzet projecten in de spotlights. Zowel gemeenten, instellingen en onderzoeks- en onderwijsinstellingen én jongvolwassenen met een beperking of met leerproblemen zijn met drie projecten aan de slag gegaan. We zetten drie projecten voor je op een rij, namelijk: Project 1: WijKringen. Een WijKring is er voor iedereen in de wijk die een hulpvraag heeft, en ook iets voor een ander wil betekenen. Een kleine groep wijkgenoten komt geregeld bijeen om samen activiteiten te ondernemen. Doel is dat mensen elkaar meer helpen, zelfstandiger worden en reguliere hulpverlening niet of minder nodig hebben. Er zijn een aantal resultaten geboekt, namelijk: meer mensen kennen elkaar. mensen gaan vaker de wijk in. mensen kijken wat er in de groep past. toekomstplan kan helpen om de visie te bepalen. bij hulpverleners moet beter bekend worden hoe het werkt en wat het kan betekenen. De WijKring is ook interessant als aanvulling op het bestaande aanbod, omdat het een andere manier is om contact te hebben in de wijk. Project 2: Omgaan met geld. Hoe kunnen jongvolwassenen beter met geld omgaan? En wat is daar voor nodig? In gesprekken met jongvolwassenen met een beperking is bekeken wat er goed gaat en wat ze moeilijk vinden. Bij alledaagse zaken, zoals boodschappen doen, of in contact met instanties. Veel jongvolwassenen geven te veel geld uit, bijvoorbeeld omdat ze niet weten wat ze hebben. Om met begeleiders over geld te praten moet er wel een 'klik' zijn. Daarnaast is het belangrijk dat begeleiders het niet helemaal van ze overnemen, maar dat ze meedenken. Een begripvolle reactie is dan extra belangrijk. De Stips Nijmegen, het Interlokaal, schuldhulpverlening en diverse vrijwilligers organisaties moeten hier verandering in brengen. Ze bieden ondersteuning bij het lezen van brieven over geldzaken en het invullen van formulieren. Project 3: Behandeling van problemen die ontstaan als je achttien wordt. In het project AanZet naar volwassenheid (18+) ligt de focus op de veranderingen rondom het 18e levensjaar. Door de vele uitdagingen die op het pad komen van een jongvolwassene (zoals je rijbewijs halen, alcohol drinken) is er behoefte aan ondersteuning maar ook om zelf aan zet te blijven. Begeleiders kunnen ondersteuning bieden door rekening te houden met onderstaande: laat jongvolwassenen tijdig, samen met ouders, begeleiders en andere betrokkenen een aantal zaken op een rij zetten. breng in kaart wat de veranderingen zijn rondom het 18e levensjaar. breng in kaart hoe zij verder willen met hun leven. breng in kaart hoe zij hun wensen kunnen realiseren, zoals hoe haalt iemand zijn/haar rijbewijs, op kamers gaan, een opleiding doen hun rijbewijs halen. Tips van ervaringsdeskundige co-onderzoekers. In alle fasen van de projecten werken jongvolwassenen met een beperking mee als co-onderzoekers. De co-onderzoekers delen adviezen over het uitvoeren van onderzoek. Ze gaven onder andere deze adviezen, namelijk: het stellen van vragen in een duidelijke taal. het interview moet niet te lang duren. dat je gesprekken beter met behulp van foto's kunt houden. dat sommige onderwerpen gevoelig liggen en dat je soms beter niet kunt doorvragen. door zelf een eigen verhaal te vertellen wordt het makkelijker voor de ander om zelf een verhaal te doen. samenwerken kost tijd en is meer dan de moeite waard. Tips en aanbevelingen vanuit de projecten. Ervaringsdeskundigen geven een aantal tips en aanbevelingen. We zetten ze voor je op een rij, namelijk: Er is behoefte aan kortdurende projecten met een concrete vraag uit de praktijk, bijvoorbeeld vanuit de gemeente, waaraan alle relevante partijen deelnemen. Het is goed als ZonMw dit kan blijven stimuleren. Het betrekken van ervaringsdeskundigen en andere partijen vraagt tijd. Neem daarom voldoende tijd om alle partijen goed te betrekken en de samenwerking te organiseren. Bron: ZonMw. Meer informatie. Nationaal Programma Gehandicapten: Gewoon Bijzonder. LVB in het Vizier (pdf). Vragenlijst LVB in het Vizier."]})

text = "Zowel gemeenten, instellingen en onderzoeks- en onderwijsinstellingen en jongvolwassenen met een beperking of met leerproblemen zijn met drie projecten aan de slag gegaan."
text = "webkit is ontwikkeld door Intel aan de Intel Open Source Technology Center."
text = "Sherpa benadrukt dat het een mooie mogelijkheid is om de gehandicaptenzorg landelijk onder de aandacht te brengen"
# text = "Sherpa benadrukt dat het een mooie mogelijkheid is om de gehandicaptenzorg landelijk onder de aandacht te brengen."
nlp_text = nlp(text)

tokens = [token for token in nlp_text]

displacy.serve(nlp_text, style='dep', port=8002)

text = "Nathan werkt al jaren met veel plezier bij BearingPoint"
doc = nlp(text)

tokens = [token.pos_ for token in doc]
[(ent.text, ent.label_) for ent in doc.ents]