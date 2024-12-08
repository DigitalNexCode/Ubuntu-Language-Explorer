import streamlit as st
from utils.database import db
from utils.audio import AudioService

# Initialize audio service
audio_service = AudioService()

def get_stories():
    return {
        "zulu": [
            {
                "title": "UMvubu noNgwenya (The Hippo and the Crocodile)",
                "content": """Long ago, uMvubu (the hippo) lived on land and ate grass. One day, he met uNgwenya (the crocodile) who invited him to swim.
                
"Woza lapha, mngani wami! (Come here, my friend!)" said uNgwenya.
"Ngiyesaba amanzi. (I'm afraid of water.)" replied uMvubu.
"Ungakhathazeki, ngizokufundisa. (Don't worry, I'll teach you.)" assured uNgwenya.

uMvubu learned to swim and loved the water so much that he now spends most of his time there!""",
                "moral": "Never be afraid to try new things!",
                "vocabulary": ["Woza - Come", "Mngani - Friend", "Amanzi - Water", "Ungakhathazeki - Don't worry"]
            },
            {
                "title": "INyoni eNcane (The Little Bird)",
                "content": """INyoni encane (the little bird) couldn't fly. Her mother said:
                
"Zama futhi! (Try again!)"
"Ngiyesaba! (I'm scared!)" said iNyoni.
"Ngiyakholwa kuwe! (I believe in you!)" her mother encouraged.

After many attempts, iNyoni finally spread her wings and soared high into the sky!""",
                "moral": "Persistence leads to success!",
                "vocabulary": ["Zama - Try", "Futhi - Again", "Ngiyakholwa - I believe", "Kuwe - In you"]
            },
            {
                "title": "UMkhulu Nemfene (The Old Man and the Monkey)",
                "content": """UMkhulu wayetshala izithelo ensimini yakhe. Ngelinye ilanga, wabona iMfene iyeba izithelo zakhe.

"Yima lapho! (Stop there!)" washo uMkhulu.
"Ngilambile! (I'm hungry!)" yaphendula iMfene.
"Uma ufuna ukudla, woza usebenze nami. (If you want food, come work with me.)" washo uMkhulu.

IMfene yasebenza noMkhulu, bese babelana ngezithelo ndawonye.""",
                "moral": "Working together is better than stealing.",
                "vocabulary": ["Yima - Stop", "Ukudla - Food", "Sebenza - Work", "Abelana - Share"]
            },
            {
                "title": "Imbali Enhle (The Beautiful Flower)",
                "content": """Kwakukhona imbali enhle kakhulu eyayikhula yodwa ehlane.

"Ngikhula ngedwa lapha. (I'm growing alone here.)" yasho imbali.
"Ungakhathazeki! (Don't worry!)" kusho inyoni.
"Ngizothatha izinhlamvu zakho ngizihambise ezindaweni ezintsha. (I'll take your seeds to new places.)"

Ngokuhamba kwesikhathi, ihlane lagcwala izimbali ezinhle.""",
                "moral": "Even small acts of kindness can create beautiful changes.",
                "vocabulary": ["Imbali - Flower", "Ihlane - Desert", "Izinhlamvu - Seeds", "Izindawo - Places"]
            },
            {
                "title": "UBhubesi Negundane (The Lion and the Mouse)",
                "content": """UBhubesi omkhulu wabamba igundane elincane.

"Ngicela ungangidli! (Please don't eat me!)" lacela igundane.
"Ngizokusiza ngelinye ilanga. (I'll help you one day.)"
"Wena? Uncane kakhulu! (You? You're too small!)" wahleka uBhubesi.

Ngelinye ilanga, uBhubesi wabanjwa othangweni. Igundane lafika lamsiza ngokuqoba intambo!""",
                "moral": "Never underestimate someone because of their size.",
                "vocabulary": ["Bhubesi - Lion", "Igundane - Mouse", "Intambo - Rope", "Siza - Help"]
            }
        ],
        "xhosa": [
            {
                "title": "UMvundla noFudo (The Rabbit and the Tortoise)",
                "content": """UMvundla wayeqhayisa ngokubaleka kakhulu. UFudo wathi:
                
"Masigijime! (Let's race!)"
"Hayi, awukwazi! (No, you can't!)" watsho uMvundla.
"Ndingakwenza! (I can do it!)" waphendula uFudo.

UFudo waphumelela kuba wayezimisele kwaye engazange ayeke!""",
                "moral": "Ukuzimisela kubalulekile! (Determination is important!)",
                "vocabulary": ["Gijima - Run", "Kwazi - Can", "Zimisela - Determined", "Phumelela - Succeed"]
            },
            {
                "title": "INkwenkwe neNkomo (The Boy and the Cow)",
                "content": """INkwenkwe yayikhathazekile kuba iNkomo yayo yayigula.

"Ndiza kukunceda. (I will help you.)" watsho uGqirha weNkomo.
"Kodwa andinamali. (But I have no money.)" yatsho iNkwenkwe.
"Ungakhathazeki, ndifuna nje uncedo lwakho esibayeni. (Don't worry, I just need your help in the kraal.)"

INkwenkwe yafunda lukhulu ngokunakekela izilwanyana.""",
                "moral": "Helping others brings unexpected rewards.",
                "vocabulary": ["Gqirha - Doctor", "Imali - Money", "Isibaya - Kraal", "Nceda - Help"]
            },
            {
                "title": "IMvula noMlimi (The Rain and the Farmer)",
                "content": """UMlimi wayelinde imvula inyanga yonke.

"Nceda, Mvula! (Please, Rain!)" wacenga uMlimi.
"Yintoni le ndiyivayo? (What do I hear?)" yabuza iMvula.
"Abantu namalima balambile. (The people and animals are hungry.)"

IMvula yeza, yonke into yaluhlaza kwakhona.""",
                "moral": "Patience and prayer can bring blessings.",
                "vocabulary": ["Mvula - Rain", "Mlimi - Farmer", "Lamba - Hungry", "Luhlaza - Green"]
            },
            {
                "title": "INtaka eKhethekileyo (The Special Bird)",
                "content": """INtaka yayingakwazi ukucula njengezinye iintaka.

"Yintoni eyam into ekhethekileyo? (What is my special thing?)" yazibuza.
"Jonga indlela othwala ngayo amanzi! (Look how you carry water!)" zatsho ezinye iintaka.

Yafumanisa ukuba yayikwazi ukunceda ezinye iintaka ngokuthwala amanzi.""",
                "moral": "Everyone has their own special talent.",
                "vocabulary": ["Ntaka - Bird", "Cula - Sing", "Amanzi - Water", "Khethekile - Special"]
            }
        ],
        "sotho": [
            {
                "title": "Tau le Tweba (The Lion and the Mouse)",
                "content": """Tau e kgolo e ne e robetse ha Tweba e nyenyane e feta.
                
"Ntšwarele! (Sorry!)" ha rialo Tweba.
"O monyenyane haholo! (You're too small!)" Tau ya tsheha.

Empa ha mohlang Tau e tshwaswa ke mahlaahlela, Tweba ya e thusa!""",
                "moral": "Se nyatse motho ka bonyenyane ba hae! (Don't judge someone by their size!)",
                "vocabulary": ["Tau - Lion", "Tweba - Mouse", "Robala - Sleep", "Thusa - Help"]
            },
            {
                "title": "Moshanyana le Pula (The Boy and the Rain)",
                "content": """Moshanyana o ne a dula tulong e omeletseng.

"Ke kopa pula! (I ask for rain!)" a rapela.
"Re lapile! (We are hungry!)" setjhaba sa rialo.
"Ke tla le thusa. (I will help you.)" Pula ya araba.

Ka tsatsi le leng, pula ya na, masimo a menya.""",
                "moral": "Thapelo e na le matla! (Prayer has power!)",
                "vocabulary": ["Pula - Rain", "Lapile - Hungry", "Thusa - Help", "Masimo - Fields"]
            },
            {
                "title": "Ntate le Kgomo (Father and the Cow)",
                "content": """Ntate o ne a na le kgomo e ntle.

"Kgomo ena ke lehlohonolo! (This cow is a blessing!)" a rialo.
"E re fa lebese le mangata. (It gives us lots of milk.)"
"Re tla e hlokomela hantle. (We will take good care of it.)"

Kgomo ya ba thusa ho fepa lelapa lohle.""",
                "moral": "Ho hlokomela diphoofolo ke bohlokwa! (Taking care of animals is important!)",
                "vocabulary": ["Kgomo - Cow", "Lebese - Milk", "Hlokomela - Take care", "Lelapa - Family"]
            },
            {
                "title": "Sefate sa Ditlhare (The Flower Tree)",
                "content": """Sefate se senyenyane se ne se sa rate ho hola.

"Hobaneng ke le monyenyane? (Why am I small?)" sa botsa.
"O sa ntse o hola! (You are still growing!)" nonyana ya araba.
"O tla ba moholo le motle! (You will be big and beautiful!)"

Ka mora dilemo, sefate sa ba seholo, se tletseng dipalesa.""",
                "moral": "Mamella, ntho tsohle di nka nako! (Be patient, everything takes time!)",
                "vocabulary": ["Sefate - Tree", "Hola - Grow", "Nonyana - Bird", "Dipalesa - Flowers"]
            }
        ],
        "tswana": [
            {
                "title": "Kgomo le Phiri (The Cow and the Wolf)",
                "content": """Kgomo e ne e fula fa Phiri e tla.
                
"Dumela, Kgomo! (Hello, Cow!)" ga bua Phiri.
"O batla eng? (What do you want?)" ga botsa Kgomo.
"Ke tshwerwe ke tlala! (I'm hungry!)" ga araba Phiri.

Kgomo ya tshaba mme ya tabogela kwa gae!""",
                "moral": "O tshwanetse go nna kelotlhoko! (You must always be careful!)",
                "vocabulary": ["Fula - Graze", "Tlala - Hunger", "Taboga - Run", "Gae - Home"]
            },
            {
                "title": "Mosetsana le Nonyane (The Girl and the Bird)",
                "content": """Mosetsana o ne a na le nonyane e e lwalang.

"O se ka wa tshwenyega! (Don't worry!)" a bolelela nonyane.
"Ke tlaa go tlhokomela! (I will take care of you!)"
"Ke a leboga! (Thank you!)" ga bua nonyane.

Morago ga malatsi, nonyane ya fola mme ya opela pina e ntle.""",
                "moral": "Lorato le tlhokomelo di folisa! (Love and care heal!)",
                "vocabulary": ["Nonyane - Bird", "Lwala - Sick", "Tlhokomela - Care for", "Opela - Sing"]
            },
            {
                "title": "Pula ya Tsholofelo (The Rain of Hope)",
                "content": """Motse o ne o le mo komelelong e kgolo.

"Re tlhoka pula! (We need rain!)" batho ba rapela.
"Tsholofelo ga e latlhiwe! (Hope is not lost!)" ga bua kgosi.
"Mmogo re ka fenya! (Together we can overcome!)"

Ka letsatsi le lengwe, pula ya na, motse wa tshela gape.""",
                "moral": "Tsholofelo le kopano di tlisa phenyo! (Hope and unity bring victory!)",
                "vocabulary": ["Pula - Rain", "Komelelo - Drought", "Kgosi - Chief", "Phenyo - Victory"]
            },
            {
                "title": "Setlhare sa Ditlhare (The Tree of Medicine)",
                "content": """Go ne go na le setlhare se se kgethegileng mo sekgweng.

"Matlhare a me a ka thusa balwetse! (My leaves can help the sick!)" sa rialo.
"Fela batho ga ba itse! (But people don't know!)"
"Ke tlaa ba bolelela! (I will tell them!)" ga bua tlhare e nnye.

Morago ga moo, batho ba simolola go dirisa ditlhare go alafa malwetse.""",
                "moral": "Kitso e tshwanetse go abiwa! (Knowledge should be shared!)",
                "vocabulary": ["Setlhare - Tree", "Matlhare - Leaves", "Balwetse - Sick people", "Alafa - Heal"]
            }
        ],
        "venda": [
            {
                "title": "Ndou na Mbevha (The Elephant and the Mouse)",
                "content": """Ndou yo vha i tshi khou tshimbila musi Mbevha i tshi mu bambela.
                
"Ndi khou humbela pfarelo! (I'm sorry!)" ya amba Mbevha.
"Ni ṱhukhu nga maanḓa! (You're too small!)" Ndou ya sea.

Fhedzi nga ḽiṅwe ḓuvha Ndou yo farwa nga vhulwadze, Mbevha ya mu thusa!""",
                "moral": "Ni songo vhuya na sasaladza muṅwe! (Never underestimate others!)",
                "vocabulary": ["Ndou - Elephant", "Mbevha - Mouse", "Tshimbila - Walk", "Thusa - Help"]
            },
            {
                "title": "Muṱhannga na Mvula (The Boy and the Rain)",
                "content": """Muṱhannga o vha a tshi dzula shangoni ḽo omaho.

"Ri ṱoḓa mvula! (We need rain!)" vhathu vha tshi lilela.
"Ndi ḓo ni thusa! (I will help you!)" ha amba Mvula.
"Ri a livhuwa! (We thank you!)" vha tshi ṱavha mukosi.

Mvula ya na, shango ḽa vha ḽitswuku.""",
                "moral": "U konḓelela hu ḓisa zwavhuḓi! (Patience brings good things!)",
                "vocabulary": ["Mvula - Rain", "Shango - Land", "Oma - Dry", "Livhuwa - Thank"]
            },
            {
                "title": "Muri wa Mitshelo (The Fruit Tree)",
                "content": """Ho vha hu na muri muhulu wo ḓala mitshelo.

"Ndi ḓo kovhela vhoṱhe! (I will share with everyone!)" wa amba.
"Fhedzi vha songo pwasha mathavhi! (But don't break branches!)"
"Ri ḓo thoma u ṱhogomela! (We will take care!)" vha fulufhedzisa.

Muri wa isa phanḓa u ṋea mitshelo miṅwaha minzhi.""",
                "moral": "U kovhela zwi ḓisa dakalo! (Sharing brings joy!)",
                "vocabulary": ["Muri - Tree", "Mitshelo - Fruits", "Mathavhi - Branches", "Ṱhogomela - Take care"]
            },
            {
                "title": "Pfuḓi na Khovhe (The Tortoise and the Fish)",
                "content": """Pfuḓi yo vha i tshi dzula tsini na tivha.

"Ndi nga si kone u bvela nnḓa ha maḓi! (I can't leave the water!)" ha amba Khovhe.
"Ndi ḓo ni sumbedza shango! (I will show you the land!)" ya fulufhedzisa Pfuḓi.
"Ni nga zwi ita hani? (How can you do it?)" Khovhe ya vhudzisa.

Pfuḓi ya ita tshiṱanga tsha maḓi kha gwada ḽayo.""",
                "moral": "Vhuṱali vhu ḓisa thandululo! (Wisdom brings solutions!)",
                "vocabulary": ["Pfuḓi - Tortoise", "Khovhe - Fish", "Tivha - Pool", "Vhuṱali - Wisdom"]
            }
        ],
        "tsonga": [
            {
                "title": "Ndlopfu na Kondlo (The Elephant and the Mouse)",
                "content": """Ndlopfu a yi famba loko Kondlo ri yi khoma.
                
"Ndzi kombela ku rivaleriwa! (I'm asking for forgiveness!)" ku vula Kondlo.
"U tsongo ngopfu! (You're too small!)" Ndlopfu yi hleka.

Kambe siku rin'wana Ndlopfu yi khomiwa hi vuvabyi, Kondlo ri yi pfuna!""",
                "moral": "U nga tekeli munhu ehansi! (Don't look down on others!)",
                "vocabulary": ["Ndlopfu - Elephant", "Kondlo - Mouse", "Famba - Walk", "Pfuna - Help"]
            },
            {
                "title": "N'wanana na Xihlovo (The Girl and the Spring)",
                "content": """N'wanana u kumile xihlovo xa mati laha ku omeke.

"Ndzi ta xi sirhelela! (I will protect it!)" a vula.
"Hi ta pfuniwa hi mati! (We will be helped by water!)"
"Hi fanele ku hlayisa! (We must preserve it!)"

Vanhu va tiko va sungule ku kuma mati yo tenga.""",
                "moral": "Ku hlayisa swipfuno i vutlhari! (Preserving resources is wisdom!)",
                "vocabulary": ["Xihlovo - Spring", "Mati - Water", "Sirhelela - Protect", "Hlayisa - Preserve"]
            },
            {
                "title": "Mpfuvu na Vurimbi (The Hippo and the Rainbow)",
                "content": """Mpfuvu a yi tshama yi ri yoxe enambyeni.

"Ndzi lava munghana! (I want a friend!)" yi rila.
"Languta ehenhla! (Look up!)" ku vula Vurimbi.
"Ndzi ta ku endlela muhlovo wo saseka! (I'll make you beautiful colors!)"

Mpfuvu yi dyondze leswaku vunghana byi ta hi tindlela to hambana.""",
                "moral": "Vunghana byi kumeka hi tindlela to tala! (Friendship comes in many ways!)",
                "vocabulary": ["Mpfuvu - Hippo", "Vurimbi - Rainbow", "Munghana - Friend", "Muhlovo - Color"]
            },
            {
                "title": "Mhandzi ya Vutlhari (The Wise Tree)",
                "content": """A ku ri na mhandzi leyikulu enhoveni.

"Tana u ta dyondza! (Come learn!)" yi vitana vana.
"Ndzi na switori swo tala! (I have many stories!)"
"Tshamani ehansi mi yingisela! (Sit down and listen!)"

Vana va dyondze swilo swo tala eka mhandzi leyi.""",
                "moral": "Vutlhari i xipfuno lexikulu! (Wisdom is a great resource!)",
                "vocabulary": ["Mhandzi - Tree", "Dyondza - Learn", "Switori - Stories", "Yingisela - Listen"]
            }
        ],
        "swati": [
            {
                "title": "Ndlovu neMpuku (The Elephant and the Mouse)",
                "content": """Ndlovu beyihamba ngesikhatsi iMpuku iyibamba.
                
"Ngiyacolisa! (I'm sorry!)" kusho iMpuku.
"Umncane kakhulu! (You're too small!)" Ndlovu yahleka.

Kodvwa ngalelinye lilanga Ndlovu yagula, iMpuku yayisita!""",
                "moral": "Ungadeleli umuntfu! (Don't underestimate a person!)",
                "vocabulary": ["Ndlovu - Elephant", "Mpuku - Mouse", "Hamba - Walk", "Sita - Help"]
            },
            {
                "title": "Umfana neLikhwezi (The Boy and the Morning Star)",
                "content": """Umfana bekavuka ekuseni kakhulu onkhe malanga.

"Ngifuna kubona likhwezi! (I want to see the morning star!)" asho.
"Likhwezi liyinkhanyeti lenhle! (The morning star is beautiful!)"
"Ngitawulinda ngize ngilibone! (I will wait until I see it!)"

Ngalelinye lilanga, wabona likhwezi likhanya kakhulu.""",
                "moral": "Kubeketela kuyasita! (Patience pays off!)",
                "vocabulary": ["Likhwezi - Morning star", "Vuka - Wake up", "Linda - Wait", "Khanya - Shine"]
            },
            {
                "title": "Imbali neLitfuba (The Flower and the Opportunity)",
                "content": """Imbali beyikhula endzaweni lebeyome kakhulu.

"Ngingakhula njani lapha? (How can I grow here?)" ibuta.
"Tfola emandla akho! (Find your strength!)" kusho umoya.
"Titfole emagcabheni akho! (Find it in your roots!)"

Imbali yakhula yaba yinhle kakhulu.""",
                "moral": "Emandla akho asekatfubeni lakho! (Your strength lies in your opportunity!)",
                "vocabulary": ["Imbali - Flower", "Khula - Grow", "Emandla - Strength", "Emagcabha - Roots"]
            },
            {
                "title": "Imvula neNkhomati (The Rain and the River)",
                "content": """INkhomati beyiphele emanti.

"Sidzinga imvula! (We need rain!)" kusho tilwane.
"Ngitawuna masinyane! (I will rain soon!)" kusho imvula.
"Lindzelani kancane! (Wait a little!)"

Ngemuva kwesikhatsi, imvula yana, iNkhomati yagcwala.""",
                "moral": "Konkhe kufika ngesikhatsi sako! (Everything comes at its time!)",
                "vocabulary": ["Imvula - Rain", "Nkhomati - River", "Linda - Wait", "Gcwala - Full"]
            }
        ],
        "ndebele": [
            {
                "title": "Indlovu neGundwane (The Elephant and the Mouse)",
                "content": """Indlovu yayihamba ngesikhathi iGundwane liyibamba.
                
"Ngiyaxolisa! (I'm sorry!)" kusho iGundwane.
"Ulincani khulu! (You're too small!)" Indlovu yahleka.

Kodwana ngelinye ilanga Indlovu yagula, iGundwane layisiza!""",
                "moral": "Ungadeleli umuntu! (Don't underestimate a person!)",
                "vocabulary": ["Indlovu - Elephant", "Gundwane - Mouse", "Hamba - Walk", "Siza - Help"]
            },
            {
                "title": "Umfana neLanga (The Boy and the Sun)",
                "content": """Umfana wayehlala ekhaya elincani ezintabeni.

"Ngifuna ukubona ilanga liphuma! (I want to see the sunrise!)" washo.
"Kufanele uvuke ekuseni! (You must wake up early!)" unina wamtjela.
"Ngizokuvuka! (I will wake up!)" wathembisa.

Ngelanga elilandelako, wabona ubuhle belanga liphuma.""",
                "moral": "Ukuzimisela kuletha impumelelo! (Determination brings success!)",
                "vocabulary": ["Ilanga - Sun", "Vuka - Wake up", "Thembisa - Promise", "Ubuhle - Beauty"]
            },
            {
                "title": "Imbali yoMvula (The Rain Flower)",
                "content": """Kwakukhona imbali eyayikhula endaweni eyomileyo.

"Ngidinga amanzi! (I need water!)" yakhala.
"Silinde imvula! (We're waiting for rain!)" ezinye iimbali zathi.
"Sizolinda ndawonye! (We will wait together!)"

Ekugcineni imvula yana, zonke iimbali zakhula zaba zinhle.""",
                "moral": "Ubudlelwano buqinisa amandla! (Unity strengthens power!)",
                "vocabulary": ["Imbali - Flower", "Amanzi - Water", "Imvula - Rain", "Linda - Wait"]
            },
            {
                "title": "Inyoni eNcani (The Little Bird)",
                "content": """Inyoni encani yayingakwazi ukuphapha.

"Ngiyesaba! (I'm afraid!)" yathi.
"Amaphiko wakho aqinile! (Your wings are strong!)" unina wathi.
"Zama godu! (Try again!)"

Ngokuzama njalo, inyoni yafunda ukuphapha phezulu esibhakabhakeni.""",
                "moral": "Ungapheli amandla, qhubeka uzama! (Don't give up, keep trying!)",
                "vocabulary": ["Inyoni - Bird", "Amaphiko - Wings", "Phapha - Fly", "Zama - Try"]
            },
            {
                "title": "UMakhulu neSivande (Grandmother and the Garden)",
                "content": """UMakhulu wayelima isivande esihle.

"Isivande sami sizopha ukudla! (My garden will give food!)" wathi.
"Singasiza ukulima? (Can we help plant?)" abantwana babuza.
"Yebo, sizolima ndawonye! (Yes, we will plant together!)"

Isivande sakhula saba sikhulu, sapha ukudla okunengi.""",
                "moral": "Ukusebenza ndawonye kuletha izithelo! (Working together brings fruits!)",
                "vocabulary": ["Isivande - Garden", "Ukudla - Food", "Lima - Plant", "Ndawonye - Together"]
            }
        ],
        "pedi": [
            {
                "title": "Tlou le Legotlo (The Elephant and the Mouse)",
                "content": """Tlou e be e sepela ge Legotlo le e swara.
                
"Ke kgopela tshwarelo! (I ask for forgiveness!)" gwa bolela Legotlo.
"O monnyane kudu! (You're too small!)" Tlou ya sega.

Efela ka letšatši le lengwe Tlou e lwala, Legotlo la e thuša!""",
                "moral": "O se nyatše motho! (Don't underestimate a person!)",
                "vocabulary": ["Tlou - Elephant", "Legotlo - Mouse", "Sepela - Walk", "Thuša - Help"]
            },
            {
                "title": "Mosetsana le Pula (The Girl and the Rain)",
                "content": """Mosetsana o be a dula nageng ye e omilego.

"Re nyaka pula! (We need rain!)" a rapela.
"Ke tla le thuša! (I will help you!)" Pula ya araba.
"Re leboga kudu! (We thank you very much!)"

Pula ya na, naga ya ba ye tala.""",
                "moral": "Go rapela go tliša mahlohonolo! (Prayer brings blessings!)",
                "vocabulary": ["Pula - Rain", "Naga - Land", "Rapela - Pray", "Tala - Green"]
            },
            {
                "title": "Mohlare wa Dienywa (The Fruit Tree)",
                "content": """Go be go na le mohlare wo mogolo wa dienywa.

"Ke tla fa bohle dienywa! (I will give everyone fruits!)" wa bolela.
"Eupša le se ke la roba makala! (But don't break branches!)"
"Re tla hlokomela! (We will take care!)" bana ba tshepiša.

Mohlare wa tšwela pele go fa dienywa mengwaga ye mentši.""",
                "moral": "Go abelana go tliša lethabo! (Sharing brings joy!)",
                "vocabulary": ["Mohlare - Tree", "Dienywa - Fruits", "Makala - Branches", "Hlokomela - Take care"]
            },
            {
                "title": "Nonyana ye Nnyane (The Little Bird)",
                "content": """Nonyana ye nnyane e be e sa kgone go fofa.

"Ke a boifa! (I'm afraid!)" ya realo.
"Maphego a gago a tiilwe! (Your wings are strong!)" mmagwe a realo.
"Leka gape! (Try again!)"

Ka go leka kgafetšakgafetša, nonyana ya ithuta go fofa godimo lefaufaung.""",
                "moral": "O se fele pelo, tšwela pele o leka! (Don't lose heart, keep trying!)",
                "vocabulary": ["Nonyana - Bird", "Maphego - Wings", "Fofa - Fly", "Leka - Try"]
            },
            {
                "title": "Koko le Tšhemo (Grandmother and the Field)",
                "content": """Koko o be a na le tšhemo ye botse.

"Tšhemo ya ka e tla re fa dijo! (My field will give us food!)" a realo.
"Re ka thuša go bjala? (Can we help plant?)" bana ba botšiša.
"Ee, re tla bjala mmogo! (Yes, we will plant together!)"

Tšhemo ya gola ya ba ye kgolo, ya fa dijo tše dintši.""",
                "moral": "Go šoma mmogo go tliša dikenywa! (Working together brings results!)",
                "vocabulary": ["Tšhemo - Field", "Dijo - Food", "Bjala - Plant", "Mmogo - Together"]
            }
        ]
    }

def display_story(story, language, story_index):
    st.subheader(story["title"])
    st.write(story["content"])
    
    # Create columns for moral and vocabulary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Moral of the Story:**")
        st.write(story["moral"])
    
    with col2:
        st.markdown("**Key Vocabulary:**")
        for word in story["vocabulary"]:
            st.write(f"• {word}")
    
    # Add audio button with unique key
    if st.button("🔊 Listen to Story", key=f"listen_{language}_{story_index}"):
        audio_content = audio_service.text_to_speech(story["content"], language)
        if audio_content:
            st.audio(audio_content)
    
    # Add mark as read button with unique key
    if st.button("Mark as Read ✅", key=f"mark_read_{language}_{story_index}"):
        if st.session_state.user:
            db.update_learning_progress(
                user_id=st.session_state.user['id'],
                resource_type="story",
                resource_id=f"{language}_{story_index}",
                progress=1.0
            )
            st.success("Story marked as read! Great job! 🌟")
        else:
            st.warning("Please sign in to track your progress.")

def kids_zone():
    st.title("👶 Kids Zone")
    st.write("Learn through fun stories in different languages!")
    
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = None
    
    # Language selection in sidebar
    st.sidebar.header("Choose Language")
    languages = {
        "zulu": "isiZulu",
        "xhosa": "isiXhosa",
        "sotho": "Sesotho",
        "tswana": "Setswana",
        "venda": "Tshivenda",
        "tsonga": "Xitsonga",
        "swati": "Siswati",
        "ndebele": "isiNdebele",
        "pedi": "Sepedi"
    }
    
    selected_language = st.sidebar.selectbox(
        "Select a language:",
        list(languages.keys()),
        format_func=lambda x: languages[x]
    )
    
    if selected_language != st.session_state.selected_language:
        st.session_state.selected_language = selected_language
        st.rerun()
    
    if not selected_language:
        st.info("👈 Please select a language from the sidebar to see stories!")
        return
    
    # Display available stories
    stories = get_stories().get(selected_language, [])
    if not stories:
        st.warning(f"No stories available in {languages[selected_language]} yet. Check back soon!")
        return
    
    st.write(f"### Stories in {languages[selected_language]}")
    
    # Display each story with progress tracking
    for i, story in enumerate(stories):
        with st.expander(f"📖 {story['title']}", expanded=i==0):
            display_story(story, selected_language, i)
        st.markdown("---")

def main():
    if 'user' not in st.session_state:
        st.session_state.user = None
    kids_zone()

if __name__ == "__main__":
    main()
