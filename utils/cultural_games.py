"""Cultural games and activities for the Ubuntu Language Explorer."""
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

class CulturalGames:
    def __init__(self):
        self.games_data = {
            "proverb_match": {
                "zulu": [
                    # Difficulty Level 1
                    {
                        "proverb": "Umuntu ngumuntu ngabantu",
                        "meaning": "A person is a person through other people",
                        "context": "This reflects the Ubuntu philosophy of interconnectedness",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Izandla ziyagezana",
                        "meaning": "Hands wash each other",
                        "context": "Emphasizes mutual help and cooperation",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Amanzi impilo",
                        "meaning": "Water is life",
                        "context": "Emphasizes the importance of water and natural resources",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Inkosi yinkosi ngabantu",
                        "meaning": "A chief is a chief through their people",
                        "context": "Leadership comes from the support of the community",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umzali uligugu",
                        "meaning": "A parent is a treasure",
                        "context": "Emphasizes the value and importance of parents",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ikhaya likhaya ngeZinsika",
                        "meaning": "A home is a home because of its pillars",
                        "context": "Family members are the foundation of a home",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Isisu somhambi asingakanani",
                        "meaning": "A traveler's stomach is not very big",
                        "context": "Be content with what your host offers when traveling",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ubucwebe obuhle buhamba ngabubili",
                        "meaning": "Beautiful beads go in pairs",
                        "context": "Good things complement each other",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Akukho ndlovu yasindwa umboko wayo",
                        "meaning": "No elephant finds its trunk too heavy",
                        "context": "Your responsibilities are yours to bear",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Injobo enhle ethungelwa ebandla",
                        "meaning": "A beautiful leopard skin is sewn in public",
                        "context": "Good work should be done transparently",
                        "difficulty": 1
                    },
                    # Difficulty Level 2
                    {
                        "proverb": "Inyoni kagcwali amakhanda amathathu",
                        "meaning": "Three bird heads cannot fit in one nest",
                        "context": "About managing resources and space wisely",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Ukupha ukuziphakela",
                        "meaning": "To give is to dish out for yourself",
                        "context": "What you give will return to you",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Imfundo umnotho wengqondo",
                        "meaning": "Education is the wealth of the mind",
                        "context": "The value of education and knowledge",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Indlela ibuzwa kwabaphambili",
                        "meaning": "The way forward is asked from those who went before",
                        "context": "Seek wisdom from elders and experienced ones",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Ikhiwane elihle ligcwala izibungu",
                        "meaning": "A beautiful fig is full of worms",
                        "context": "Appearances can be deceiving",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Umuthi ugotshwa usemanzi",
                        "meaning": "A tree is bent while still young",
                        "context": "Children should be taught good values early",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Inkunzi isematholeni",
                        "meaning": "The bull is among the calves",
                        "context": "Future leaders are found among the youth",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Imbila yeswela umsila ngokulayezela",
                        "meaning": "The rock rabbit lacks a tail because of sending others",
                        "context": "Do important things yourself rather than delegating",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Amageja alingana nokuphakwa",
                        "meaning": "Hoes are equal to being dished for",
                        "context": "You reap what you sow",
                        "difficulty": 2
                    },
                    {
                        "proverb": "Umkhombe uwela abantu bemnyama",
                        "meaning": "The boat sinks with black people",
                        "context": "Misfortune doesn't discriminate",
                        "difficulty": 2
                    },
                    # Difficulty Level 3
                    {
                        "proverb": "Isizwe sigotywa siphethe inkatha",
                        "meaning": "A nation is bent while holding its grass ring",
                        "context": "Complex problems require careful handling",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Umuntu akalahlwa",
                        "meaning": "A person is not thrown away",
                        "context": "Everyone deserves second chances",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Inhlamba iphehlwa ebandla",
                        "meaning": "Insults are churned in public",
                        "context": "Conflicts should be resolved openly",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Inyoni yakhela ngamaqubu enye",
                        "meaning": "A bird builds with another's feathers",
                        "context": "We progress through mutual support",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Ubuhle bendoda ziinkomo zayo",
                        "meaning": "A man's beauty is his cattle",
                        "context": "True worth lies in one's achievements",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Ihlonipha laphokuvela khona",
                        "meaning": "It (respect) comes from where it originates",
                        "context": "Respect is reciprocal",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Umthente uhlaba usamila",
                        "meaning": "The grass blade pierces while growing",
                        "context": "Early signs predict future behavior",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Isalakutshelwa sibona ngomopho",
                        "meaning": "The stubborn one learns by the flow of blood",
                        "context": "Those who don't take advice learn through hardship",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Ingwe idla ngamabala",
                        "meaning": "The leopard is respected for its spots",
                        "context": "Character and reputation matter",
                        "difficulty": 3
                    },
                    {
                        "proverb": "Akukho ntaka inokubhabha ngephiko elinye",
                        "meaning": "No bird can fly with one wing",
                        "context": "Success requires cooperation and support",
                        "difficulty": 3
                    }
                ],
                "xhosa": [
                    {
                        "proverb": "Umntu ngumntu ngabantu",
                        "meaning": "A person is a person through other people",
                        "context": "Similar to Zulu, emphasizing community",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Isandla sihlamba esinye",
                        "meaning": "One hand washes the other",
                        "context": "About mutual assistance and reciprocity",
                        "difficulty": 1
                    },
                ],
                "ndebele": [
                    {
                        "proverb": "Indlela ibuzwa kwabaphambili",
                        "meaning": "The way forward is asked from those who went before",
                        "context": "About learning from elders and experience",
                        "difficulty": 1
                    }
                ],
                "pedi": [
                    {
                        "proverb": "Tau tša hloka seboka di šitwa ke nare e hlotša",
                        "meaning": "Lions that lack unity are defeated by a limping buffalo",
                        "context": "About the importance of unity and cooperation",
                        "difficulty": 1
                    }
                ],
                "sotho": [
                    {
                        "proverb": "Matsoho a hlatswana",
                        "meaning": "Hands wash each other",
                        "context": "About mutual help and cooperation",
                        "difficulty": 1
                    }
                ],
                "swati": [
                    {
                        "proverb": "Injobo itfungelwa ebandla",
                        "meaning": "A leopard's skin is sewn in public",
                        "context": "About transparency and community involvement",
                        "difficulty": 1
                    }
                ],
                "tsonga": [
                    {
                        "proverb": "Vuxokoxoko byi dlaya nhongana",
                        "meaning": "Too much detail kills the beetle",
                        "context": "About being concise and direct",
                        "difficulty": 1
                    }
                ],
                "tswana": [
                    {
                        "proverb": "Motho ke motho ka batho",
                        "meaning": "A person is a person through others",
                        "context": "Ubuntu philosophy in Setswana culture",
                        "difficulty": 1
                    }
                ],
                "venda": [
                    {
                        "proverb": "Muthu ndi muthu nga vhathu",
                        "meaning": "A person is a person through other people",
                        "context": "About Ubuntu and human interdependence",
                        "difficulty": 1
                    }
                ],
                "afrikaans": [
                    {
                        "proverb": "'n Boer maak 'n plan",
                        "meaning": "A farmer makes a plan",
                        "context": "About resourcefulness and problem-solving",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Alle baat help",
                        "meaning": "Every little bit helps",
                        "context": "About the value of small contributions",
                        "difficulty": 1
                    },
                ],
                "sesotho": [
                    {
                        "proverb": "Motho ke motho ka batho",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in Sesotho culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Matsoho a lemisetsa hloho",
                        "meaning": "Hands work for the head",
                        "context": "Hard work brings success",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Nonyana e haela ka tsiba tsa e nngwe",
                        "meaning": "A bird builds with another bird's feathers",
                        "context": "Success comes through cooperation",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mphato o tswala ngwana",
                        "meaning": "Unity breeds success",
                        "context": "Working together leads to achievement",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Letsatsi le tjhaba le dikgomo",
                        "meaning": "The sun rises with the cattle",
                        "context": "Early rising brings prosperity",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mmangwana o tshwara thipa ka bohaleng",
                        "meaning": "A mother holds the knife by its sharp edge",
                        "context": "Parents make sacrifices for their children",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ntja-pedi ha e hlolwe ke sebata",
                        "meaning": "Two dogs cannot be defeated by a wild animal",
                        "context": "Unity brings strength",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Moketa ho tsoswa o itsosang",
                        "meaning": "Help is given to those who help themselves",
                        "context": "Self-initiative attracts support",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Sejeso ha se fete molomo",
                        "meaning": "Food doesn't pass the mouth",
                        "context": "Opportunity should be seized when it comes",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Thuto ke lesedi la bophelo",
                        "meaning": "Education is the light of life",
                        "context": "Education brings enlightenment",
                        "difficulty": 1
                    }
                ],
                "setswana": [
                    {
                        "proverb": "Motho ke motho ka batho",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in Setswana culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Kgetsi ya tsie e kgonwa ke go tshwaraganelwa",
                        "meaning": "A bag of locusts is manageable when tackled together",
                        "context": "Unity makes difficult tasks easier",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Sedikwa ke ntšwa pedi ga se thata",
                        "meaning": "That which is pursued by two dogs is easily caught",
                        "context": "Cooperation makes work easier",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mabogo dinku a thebana",
                        "meaning": "Hands are sheep, they wash each other",
                        "context": "People must help each other",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Lobelo ga se molemo",
                        "meaning": "Speed is not medicine",
                        "context": "Rushing doesn't solve problems",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Pula e a na, macholo a a lla",
                        "meaning": "When it rains, the frogs croak",
                        "context": "Everything has its time",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Moremogolo go betlwa wa taola",
                        "meaning": "The big tree is carved to make dice",
                        "context": "Great things take time and effort",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Lore lo ojwa lo sa le metsi",
                        "meaning": "A stick is bent while still wet",
                        "context": "Children should be taught while young",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Tau e senang seboka e siiwa ke none e tlhotsa",
                        "meaning": "Lions without unity are defeated by a limping buffalo",
                        "context": "Unity brings strength",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mosadi tshwene o jewa mabogo",
                        "meaning": "A woman baboon is eaten for her hands",
                        "context": "Hard work brings rewards",
                        "difficulty": 1
                    }
                ],
                "tshivenda": [
                    {
                        "proverb": "Muthu ndi muthu nga vhathu",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in Tshivenda culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Munwe muthihi a u tusi mathuthu",
                        "meaning": "One finger cannot pick up grain",
                        "context": "Unity and cooperation are essential",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Vhana vha nwana ndi vhana",
                        "meaning": "Your child's children are your children",
                        "context": "Family responsibility extends to all generations",
                        "difficulty": 1
                    },
                    {
                        "proverb": "U kanda tshisima a u tshi vhoni",
                        "meaning": "You don't see the spring while stepping on it",
                        "context": "Value what you have before it's gone",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Tshinoni tshihulwane tshi fhufhela ntha ha miri",
                        "meaning": "A big bird flies above the trees",
                        "context": "Great people achieve great things",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mutukana wa ndou ha tshimbili e ethe",
                        "meaning": "A young elephant doesn't walk alone",
                        "context": "Young ones need guidance",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mulimo wa tshikolodo a u na murunzi",
                        "meaning": "The spirit of debt has no shadow",
                        "context": "Debt follows you everywhere",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Hu na maduvha a u kanda na a u kandwa",
                        "meaning": "There are days to step on others and days to be stepped on",
                        "context": "Life has its ups and downs",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mutsindo wa mbilu a u pfali",
                        "meaning": "The sound of the heart is not heard",
                        "context": "True feelings are often hidden",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Muthu ha langi nga luvhala",
                        "meaning": "A person is not judged by color",
                        "context": "Character matters more than appearance",
                        "difficulty": 1
                    }
                ],
                "xitsonga": [
                    {
                        "proverb": "Munhu i munhu hi vanhu",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in Xitsonga culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Tinyarhi ti dlaya nyoka",
                        "meaning": "Buffalo kill the snake",
                        "context": "Unity brings strength",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Rihlampfu rin'we a ri peli hove",
                        "meaning": "One stick cannot kill a fish",
                        "context": "Cooperation is necessary for success",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Xandla xa hlamba xin'wana",
                        "meaning": "One hand washes the other",
                        "context": "Mutual help is essential",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ku tlula ka mhala ku letela n'wana",
                        "meaning": "The jumping of the impala teaches its young",
                        "context": "Children learn from their parents",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ndlopfu yi dlaya hi risokoti",
                        "meaning": "An elephant can be killed by an ant",
                        "context": "Don't underestimate small things",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Vuxika byi tiva hi timpfula",
                        "meaning": "Winter is known by its rains",
                        "context": "Things are known by their results",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ku pfumala i ku dyondza",
                        "meaning": "To lack is to learn",
                        "context": "Hardship teaches valuable lessons",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Mhaka yi vula hi loyi a yi vonaka",
                        "meaning": "A matter is told by the one who sees it",
                        "context": "First-hand experience matters",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Tihlo ra nghala ri vona swa le kule",
                        "meaning": "The eye of the lion sees far",
                        "context": "Leaders must have vision",
                        "difficulty": 1
                    }
                ],
                "siswati": [
                    {
                        "proverb": "Umuntfu ngumuntfu ngebantfu",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in siSwati culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Tandla tiyagezana",
                        "meaning": "Hands wash each other",
                        "context": "People help each other to succeed",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Inkhosi yinkhosi ngebantfu",
                        "meaning": "A king is a king through his people",
                        "context": "Leadership depends on followers",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umtfombi ugcoka lubisi lwakhe",
                        "meaning": "A maiden wears her own milk",
                        "context": "Be proud of who you are",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ingwenya ihlala emantini",
                        "meaning": "A crocodile stays in water",
                        "context": "Stay true to your nature",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Indlela ibutwa kulapambili",
                        "meaning": "The road is asked from those ahead",
                        "context": "Seek wisdom from those with experience",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umkhulu uhlala etfundzini",
                        "meaning": "An elder sits in the shade",
                        "context": "Respect comes with age and wisdom",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Inkhomo iyalala ishiye umtfunti",
                        "meaning": "A cow lies down leaving its shadow",
                        "context": "Your legacy lives on after you",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Libhungane liyawulibona umphonjwana walo",
                        "meaning": "A beetle sees its own little horn",
                        "context": "Be aware of your own strengths",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umfula udzabuka lapho ungajulanga khona",
                        "meaning": "The river breaks where it's shallow",
                        "context": "Problems often arise where least expected",
                        "difficulty": 1
                    }
                ],
                "isindebele": [
                    {
                        "proverb": "Umuntu ngumuntu ngabantu",
                        "meaning": "A person is a person through other people",
                        "context": "Ubuntu philosophy in isiNdebele culture",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Izandla ziyagezana",
                        "meaning": "Hands wash each other",
                        "context": "Mutual cooperation is essential",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Indlela ibuza kwabaphambili",
                        "meaning": "The way forward is asked from those ahead",
                        "context": "Learn from those with experience",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umzali uligugu",
                        "meaning": "A parent is a treasure",
                        "context": "Value and respect parents",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ihlonipha lapho ingayi khona",
                        "meaning": "It (respect) extends even where you won't go",
                        "context": "Respect has no boundaries",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Isikhumba sigoqwa sisemanzi",
                        "meaning": "A hide is folded while still wet",
                        "context": "Train children while they're young",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Imbila yaswela umsila ngokulayezela",
                        "meaning": "The rock rabbit lost its tail by sending others",
                        "context": "Do important things yourself",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Ikosi yikosi ngabantu",
                        "meaning": "A king is a king through people",
                        "context": "Leadership requires followers",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umhlobo wami ngumhlobo wakho",
                        "meaning": "My friend is your friend",
                        "context": "Friendship extends through connections",
                        "difficulty": 1
                    },
                    {
                        "proverb": "Umuntu akalahlwa",
                        "meaning": "A person is not thrown away",
                        "context": "Every person has value",
                        "difficulty": 1
                    }
                ]
            },
            "cultural_quiz": {
                "zulu": [
                    {
                        "stage": 1,
                        "question": "What is the significance of 'Ubuntu' in Zulu culture?",
                        "options": [
                            "A type of traditional food",
                            "A philosophy of human interconnectedness",
                            "A traditional dance",
                            "A type of clothing"
                        ],
                        "correct": 1,
                        "explanation": "Ubuntu is a philosophy that emphasizes our interconnectedness - 'I am because we are'",
                        "difficulty": 1
                    },
                    {
                        "stage": 2,
                        "question": "What is the traditional Zulu greeting?",
                        "options": [
                            "Sawubona",
                            "Hello",
                            "Dumela",
                            "Molo"
                        ],
                        "correct": 0,
                        "explanation": "Sawubona literally means 'I see you' and is a sign of respect and recognition",
                        "difficulty": 1
                    },
                    {
                        "stage": 3,
                        "question": "What is 'imvunulo'?",
                        "options": [
                            "A traditional Zulu dance",
                            "Traditional Zulu attire",
                            "A Zulu ceremony",
                            "A type of food"
                        ],
                        "correct": 1,
                        "explanation": "Imvunulo refers to traditional Zulu clothing worn during ceremonies",
                        "difficulty": 1
                    },
                    {
                        "stage": 4,
                        "question": "What is 'umqombothi'?",
                        "options": [
                            "A traditional beer",
                            "A type of dance",
                            "A ceremony",
                            "A musical instrument"
                        ],
                        "correct": 0,
                        "explanation": "Umqombothi is a traditional Zulu beer made from sorghum malt",
                        "difficulty": 1
                    },
                    {
                        "stage": 5,
                        "question": "What is the significance of 'lobola' in Zulu culture?",
                        "options": [
                            "A traditional dance",
                            "A type of food",
                            "Bride price/dowry",
                            "A musical instrument"
                        ],
                        "correct": 2,
                        "explanation": "Lobola is a traditional practice where the groom's family pays respect to the bride's family",
                        "difficulty": 1
                    },
                    {
                        "stage": 1,
                        "question": "What is 'indlamu'?",
                        "options": [
                            "A traditional war dance",
                            "A type of food",
                            "A ceremony",
                            "A musical instrument"
                        ],
                        "correct": 0,
                        "explanation": "Indlamu is a traditional Zulu war dance performed at ceremonies",
                        "difficulty": 2
                    }
                ],
                "xhosa": [
                    {
                        "stage": 1,
                        "question": "What is the significance of 'Ulwaluko' in Xhosa culture?",
                        "options": [
                            "A traditional dance",
                            "A coming of age ceremony for young men",
                            "A type of traditional food",
                            "A festival"
                        ],
                        "correct": 1,
                        "explanation": "Ulwaluko is an important initiation ritual marking the transition to manhood",
                        "difficulty": 2
                    },
                    {
                        "stage": 2,
                        "question": "What is 'umqombothi' in Xhosa culture?",
                        "options": [
                            "Traditional beer made from maize and sorghum",
                            "A type of traditional dress",
                            "A wedding ceremony",
                            "A traditional musical instrument"
                        ],
                        "correct": 0,
                        "explanation": "Umqombothi is a traditional beer made from maize and sorghum malt, often used in ceremonies",
                        "difficulty": 1
                    },
                    {
                        "stage": 3,
                        "question": "What is the significance of 'intonjane'?",
                        "options": [
                            "A traditional weapon",
                            "A coming of age ceremony for young women",
                            "A type of traditional food",
                            "A harvest festival"
                        ],
                        "correct": 1,
                        "explanation": "Intonjane is a traditional ceremony marking a young woman's transition to womanhood",
                        "difficulty": 2
                    },
                    {
                        "stage": 4,
                        "question": "What is 'isiXhosa isiduko'?",
                        "options": [
                            "A traditional dance",
                            "A clan name",
                            "A type of food",
                            "A musical instrument"
                        ],
                        "correct": 1,
                        "explanation": "Isiduko is a clan name that helps trace family lineage and determines certain cultural practices",
                        "difficulty": 2
                    },
                    {
                        "stage": 5,
                        "question": "What is 'ukuthwala' in traditional Xhosa culture?",
                        "options": [
                            "A traditional dance",
                            "A marriage custom",
                            "A harvest ceremony",
                            "A type of traditional dress"
                        ],
                        "correct": 1,
                        "explanation": "Ukuthwala is a traditional form of marriage negotiation, though its practice has evolved over time",
                        "difficulty": 3
                    },
                    {
                        "stage": 1,
                        "question": "What is the meaning of 'Ubuntu' in Xhosa philosophy?",
                        "options": [
                            "Personal success",
                            "Individual achievement",
                            "Human interconnectedness",
                            "Material wealth"
                        ],
                        "correct": 2,
                        "explanation": "Ubuntu emphasizes that a person is a person through other people - 'umntu ngumntu ngabantu'",
                        "difficulty": 1
                    }
                ],
            },
            "story_completion": {
                "zulu": [
                    {
                        "stage": 1,
                        "title": "UNogwaja neNdlovu",
                        "content": "Kudala kwakukhona uNogwaja ohlakaniphile ne{missing1}enkulu. UNogwaja wayefuna ukubonisa i{missing2} ukuthi yize emncane kodwa u{missing3}.",
                        "missing_parts": [
                            {
                                "position": 1,
                                "options": ["Ndlovu", "Bhubesi", "Mpisi"],
                                "correct": "Ndlovu",
                                "context": "The story is about a rabbit and an elephant"
                            }
                        ],
                        "difficulty": 1
                    }
                ],
                "xhosa": [
                    {
                        "stage": 1,
                        "title": "UMvula noMoya",
                        "content": "Kudala kwakho u{missing1} noMoya besixabana ngokuba ngubani ona{missing2} kunomnye. Bafika indoda ithwele i{missing3}.",
                        "missing_parts": [
                            {
                                "position": 1,
                                "options": ["Mvula", "Langa", "Nyanga"],
                                "correct": "Mvula",
                                "context": "The story is about Rain and Wind"
                            },
                            {
                                "position": 2,
                                "options": ["mandla", "thanda", "hamba"],
                                "correct": "mandla",
                                "context": "They were arguing about who was stronger"
                            },
                            {
                                "position": 3,
                                "options": ["jezi", "bhanti", "nqayi"],
                                "correct": "jezi",
                                "context": "The person was wearing a jersey"
                            }
                        ],
                        "difficulty": 1
                    },
                    {
                        "stage": 2,
                        "title": "Imbila yesingxobo",
                        "content": "Kudala kwakukho i{missing1} eyayihlala e{missing2}. Yayingafuni uku{missing3} njengezinye izilwanyana.",
                        "missing_parts": [
                            {
                                "position": 1,
                                "options": ["mbila", "nkawu", "ngwenya"],
                                "correct": "mbila",
                                "context": "The story is about a rock rabbit"
                            },
                            {
                                "position": 2,
                                "options": ["mngxumeni", "hlathini", "mlanjeni"],
                                "correct": "mngxumeni",
                                "context": "The animal lived in a hole"
                            },
                            {
                                "position": 3,
                                "options": ["sebenza", "dlala", "cula"],
                                "correct": "sebenza",
                                "context": "The animal didn't want to work"
                            }
                        ],
                        "difficulty": 2
                    },
                    {
                        "stage": 3,
                        "title": "Unogwaja neNkukhu",
                        "content": "U{missing1} wayehleka i{missing2} ngoba ingazange i{missing3} ukuba izukulwana zayo zizodla ntoni.",
                        "missing_parts": [
                            {
                                "position": 1,
                                "options": ["nogwaja", "mpuku", "ngwenya"],
                                "correct": "nogwaja",
                                "context": "The story is about a rabbit"
                            },
                            {
                                "position": 2,
                                "options": ["nkukhu", "nkawu", "ndlovu"],
                                "correct": "nkukhu",
                                "context": "The rabbit was laughing at a chicken"
                            },
                            {
                                "position": 3,
                                "options": ["cinge", "hambe", "dlale"],
                                "correct": "cinge",
                                "context": "The chicken didn't think about the future"
                            }
                        ],
                        "difficulty": 2
                    }
                ],
            },
            "word_association": {
                "zulu": [
                    {
                        "stage": 1,
                        "category": "Family",
                        "words": [
                            ("ubaba", "father"),
                            ("umama", "mother"),
                            ("udadewethu", "sister"),
                            ("umfowethu", "brother"),
                            ("ugogo", "grandmother")
                        ],
                        "difficulty": 1
                    }
                ],
            },
            "sign_language_practice": {
                "sasl": [
                    {
                        "stage": 1,
                        "category": "Basic Signs",
                        "signs": [
                            {
                                "word": "hello",
                                "video_url": "signs/hello.mp4",
                                "description": "Wave your hand side to side near your face",
                                "practice_tips": "Keep your palm facing forward, fingers slightly spread"
                            },
                            {
                                "word": "thank you",
                                "video_url": "signs/thank_you.mp4",
                                "description": "Touch your chin with your fingertips, then move your hand forward",
                                "practice_tips": "Keep your movement smooth and deliberate"
                            }
                        ],
                        "difficulty": 1
                    },
                    {
                        "stage": 1,
                        "category": "Numbers",
                        "signs": [
                            {
                                "word": "one",
                                "video_url": "signs/one.mp4",
                                "description": "Hold up your index finger",
                                "practice_tips": "Keep other fingers closed"
                            },
                            {
                                "word": "two",
                                "video_url": "signs/two.mp4",
                                "description": "Hold up your index and middle fingers",
                                "practice_tips": "Keep fingers together"
                            }
                        ],
                        "difficulty": 2
                    }
                ]
            },
            "memory_match": {
                "zulu": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"sawubona": "hello"},
                            {"unjani": "how are you"},
                            {"ngiyaphila": "I am fine"},
                            {"sala kahle": "stay well (goodbye)"},
                            {"hamba kahle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "xhosa": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"molo": "hello"},
                            {"unjani": "how are you"},
                            {"ndiphilile": "I am fine"},
                            {"sala kakuhle": "stay well (goodbye)"},
                            {"hamba kakuhle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "ndebele": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"lotjhani": "hello"},
                            {"unjani": "how are you"},
                            {"ngiyaphila": "I am fine"},
                            {"sala kuhle": "stay well (goodbye)"},
                            {"hamba kuhle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "pedi": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"dumela": "hello"},
                            {"o kae": "how are you"},
                            {"ke gabotse": "I am fine"},
                            {"sala gabotse": "stay well (goodbye)"},
                            {"sepela gabotse": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "sotho": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"dumela": "hello"},
                            {"u phela joang": "how are you"},
                            {"ke phela hantle": "I am fine"},
                            {"sala hantle": "stay well (goodbye)"},
                            {"tsamaea hantle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "swati": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"sawubona": "hello"},
                            {"unjani": "how are you"},
                            {"ngiyaphila": "I am fine"},
                            {"sala kahle": "stay well (goodbye)"},
                            {"hamba kahle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "tsonga": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"avuxeni": "hello"},
                            {"u njhani": "how are you"},
                            {"ndzi kahle": "I am fine"},
                            {"sala kahle": "stay well (goodbye)"},
                            {"famba kahle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "tswana": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"dumela": "hello"},
                            {"o kae": "how are you"},
                            {"ke teng": "I am fine"},
                            {"sala sentle": "stay well (goodbye)"},
                            {"tsamaya sentle": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "venda": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"ndaa": "hello"},
                            {"ni khou ita zwone": "how are you"},
                            {"ndi khou tshila zwavhudi": "I am fine"},
                            {"sala zwavhudi": "stay well (goodbye)"},
                            {"tshimbila zwavhudi": "go well (goodbye)"}
                        ],
                        "difficulty": 1
                    }
                ],
                "afrikaans": [
                    {
                        "category": "Greetings",
                        "pairs": [
                            {"hallo": "hello"},
                            {"hoe gaan dit": "how are you"},
                            {"goed dankie": "fine thank you"},
                            {"totsiens": "goodbye"},
                            {"lekker dag": "nice day"}
                        ],
                        "difficulty": 1
                    }
                ]
            }
        }

    def get_game_content(self, game_type: str, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get content for a specific game type, language, difficulty level, and stage."""
        if game_type not in self.games_data:
            return {"error": "Game type not found"}
            
        if language not in self.games_data[game_type]:
            return {"error": "Language not supported for this game"}
            
        game_content = self.games_data[game_type][language]
        
        # Filter by difficulty and stage
        filtered_content = [
            item for item in game_content 
            if item.get("difficulty", 1) == difficulty and item.get("stage", 1) == stage
        ]
        
        if not filtered_content:
            return {"error": f"No content available for difficulty level {difficulty}, stage {stage}"}
            
        return {
            "type": game_type,
            "language": language,
            "difficulty": difficulty,
            "stage": stage,
            "content": filtered_content
        }

    def get_available_stages(self, game_type: str, language: str, difficulty: int = 1) -> List[int]:
        """Get available stages for a specific game type, language, and difficulty level."""
        if game_type not in self.games_data or language not in self.games_data[game_type]:
            return []
            
        content = self.games_data[game_type][language]
        stages = [
            item.get("stage", 1) 
            for item in content 
            if item.get("difficulty", 1) == difficulty
        ]
        return sorted(list(set(stages)))

    def get_max_difficulty(self, game_type: str, language: str) -> int:
        """Get the maximum difficulty level available for a game type and language."""
        if game_type not in self.games_data or language not in self.games_data[game_type]:
            return 1
            
        content = self.games_data[game_type][language]
        difficulties = [item.get("difficulty", 1) for item in content]
        return max(difficulties) if difficulties else 1

    def get_proverb_game(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get proverb matching game content."""
        return self.get_game_content("proverb_match", language, difficulty, stage)

    def get_cultural_quiz(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get cultural quiz content."""
        return self.get_game_content("cultural_quiz", language, difficulty, stage)

    def get_story_completion(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get story completion game content."""
        return self.get_game_content("story_completion", language, difficulty, stage)

    def get_word_association(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get word association game content."""
        return self.get_game_content("word_association", language, difficulty, stage)

    def get_memory_match(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get memory match game content."""
        return self.get_game_content("memory_match", language, difficulty, stage)

    def get_sign_language_practice(self, language: str, difficulty: int = 1, stage: int = 1) -> Dict[str, Any]:
        """Get sign language practice game content."""
        return self.get_game_content("sign_language_practice", language, difficulty, stage)

    def get_available_games(self, language: str = None) -> List[Dict[str, Any]]:
        """Get list of available games, optionally filtered by language."""
        games = [
            {
                "id": "proverb_match",
                "title": "Match the Proverbs",
                "description": "Learn traditional proverbs and their meanings",
                "difficulty": 1,
                "languages": list(self.games_data["proverb_match"].keys())
            },
            {
                "id": "cultural_quiz",
                "title": "Cultural Knowledge Quiz",
                "description": "Test your knowledge of cultural traditions",
                "difficulty": 2,
                "languages": list(self.games_data["cultural_quiz"].keys())
            },
            {
                "id": "story_completion",
                "title": "Complete the Story",
                "description": "Practice language by completing traditional stories",
                "difficulty": 2,
                "languages": list(self.games_data["story_completion"].keys())
            },
            {
                "id": "word_association",
                "title": "Word Association",
                "description": "Learn words by category and association",
                "difficulty": 1,
                "languages": list(self.games_data["word_association"].keys())
            },
            {
                "id": "memory_match",
                "title": "Memory Match",
                "description": "Match pairs of words to improve vocabulary",
                "difficulty": 1,
                "languages": list(self.games_data["memory_match"].keys())
            },
            {
                "id": "sign_language_practice",
                "title": "Sign Language Practice",
                "description": "Practice basic signs in South African Sign Language",
                "difficulty": 1,
                "languages": list(self.games_data["sign_language_practice"].keys())
            }
        ]
        
        if language:
            return [game for game in games if language in game["languages"]]
        return games

    def check_answer(self, game_type: str, language: str, question_id: int, answer: str) -> Dict[str, Any]:
        """Check if an answer is correct for a given game question."""
        game_content = self.games_data.get(game_type, {}).get(language, [])
        if not game_content or question_id >= len(game_content):
            return {"error": "Invalid question"}
            
        question = game_content[question_id]
        is_correct = False
        
        if game_type == "proverb_match":
            is_correct = answer.lower() == question["meaning"].lower()
        elif game_type == "cultural_quiz":
            is_correct = answer == question["options"][question["correct"]]
        elif game_type == "story_completion":
            for part in question["missing_parts"]:
                if part["position"] == question_id:
                    is_correct = answer == part["correct"]
                    break
        
        return {
            "correct": is_correct,
            "explanation": question.get("explanation", ""),
            "context": question.get("context", "")
        }

    def get_achievements(self, user_progress: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get achievements based on user progress."""
        achievements = []
        
        # Example achievement criteria
        if user_progress.get("games_played", 0) >= 10:
            achievements.append({
                "id": "games_10",
                "title": "Game Explorer",
                "description": "Played 10 different games",
                "icon": "🎮"
            })
            
        if user_progress.get("proverbs_learned", 0) >= 5:
            achievements.append({
                "id": "proverbs_5",
                "title": "Wisdom Seeker",
                "description": "Learned 5 traditional proverbs",
                "icon": "📚"
            })
            
        return achievements
