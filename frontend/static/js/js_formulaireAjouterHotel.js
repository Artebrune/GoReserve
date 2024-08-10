var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");
var form_3 = document.querySelector(".form_3");


var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");
var form_3_btns = document.querySelector(".form_3_btns");


var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");
var form_2_next_btn = document.querySelector(".form_2_btns .btn_next");
var form_3_back_btn = document.querySelector(".form_3_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");
var form_3_progessbar = document.querySelector(".form_3_progessbar");

var btn_done = document.querySelector(".btn_done");
var modal_wrapper = document.querySelector(".modal_wrapper");
var shadow = document.querySelector(".shadow");

form_1_next_btn.addEventListener("click", function(){
	form_1.style.display = "none";
	form_2.style.display = "block";

	form_1_btns.style.display = "none";
	form_2_btns.style.display = "flex";

	form_2_progessbar.classList.add("active");
});

form_2_back_btn.addEventListener("click", function(){
	form_1.style.display = "block";
	form_2.style.display = "none";

	form_1_btns.style.display = "flex";
	form_2_btns.style.display = "none";

	form_2_progessbar.classList.remove("active");
});

form_2_next_btn.addEventListener("click", function(){
	form_2.style.display = "none";
	form_3.style.display = "block";

	form_3_btns.style.display = "flex";
	form_2_btns.style.display = "none";

	form_3_progessbar.classList.add("active");
});

form_3_back_btn.addEventListener("click", function(){
	form_2.style.display = "block";
	form_3.style.display = "none";

	form_3_btns.style.display = "none";
	form_2_btns.style.display = "flex";

	form_3_progessbar.classList.remove("active");
});

btn_done.addEventListener("click", function(){
	modal_wrapper.classList.add("active");
})

shadow.addEventListener("click", function(){
	modal_wrapper.classList.remove("active");
})

document.getElementById('pays').addEventListener('change', function() {
	var countryPhoneCodes = {
		"Afghanistan": "+93", "Albanie": "+355", "Algérie": "+213", "Andorre": "+376", "Angola": "+244", "Antigua-et-Barbuda": "+1-268",
	"Argentine": "+54", "Arménie": "+374", "Australie": "+61", "Autriche": "+43", "Azerbaïdjan": "+994", "Bahamas": "+1-242",
	"Bahreïn": "+973", "Bangladesh": "+880", "Barbade": "+1-246", "Biélorussie": "+375", "Belgique": "+32", "Belize": "+501",
	"Bénin": "+229", "Bhoutan": "+975", "Bolivie": "+591", "Botswana": "+267", "Brésil": "+55", "Brunei": "+673", "Bulgarie": "+359",
	"Burkina Faso": "+226", "Burundi": "+257", "Cabo Verde": "+238", "Cambodge": "+855", "Cameroun": "+237", "Canada": "+1",
	"Centrafrique": "+236", "Chili": "+56", "Chine": "+86", "Colombie": "+57", "Comores": "+269", "Congo": "+242",
	"République démocratique du Congo": "+243", "Costa Rica": "+506", "Croatie": "+385", "Cuba": "+53", "Chypre": "+357",
	"République tchèque": "+420", "Danemark": "+45", "Djibouti": "+253", "Dominique": "+1-767", "République dominicaine": "+1-809",
	"Équateur": "+593", "Égypte": "+20", "El Salvador": "+503", "Guinée équatoriale": "+240", "Érythrée": "+291", "Estonie": "+372",
	"Eswatini": "+268", "Éthiopie": "+251", "Fidji": "+679", "Finlande": "+358", "France": "+33", "Gabon": "+241", "Gambie": "+220",
	"Géorgie": "+995", "Allemagne": "+49", "Ghana": "+233", "Grèce": "+30", "Grenade": "+1-473", "Guatemala": "+502", "Guinée": "+224",
	"Guinée-Bissau": "+245", "Guyana": "+592", "Haïti": "+509", "Honduras": "+504", "Hongrie": "+36", "Islande": "+354", "Inde": "+91",
	"Indonésie": "+62", "Iran": "+98", "Irak": "+964", "Irlande": "+353", "Israël": "+972", "Italie": "+39", "Jamaïque": "+1-876",
	"Japon": "+81", "Jordanie": "+962", "Kazakhstan": "+7", "Kenya": "+254", "Kiribati": "+686", "Corée du Nord": "+850",
	"Corée du Sud": "+82", "Kosovo": "+383", "Koweït": "+965", "Kirghizistan": "+996", "Laos": "+856", "Lettonie": "+371", "Liban": "+961",
	"Lesotho": "+266", "Libéria": "+231", "Libye": "+218", "Liechtenstein": "+423", "Lituanie": "+370", "Luxembourg": "+352",
	"Madagascar": "+261", "Malawi": "+265", "Malaisie": "+60", "Maldives": "+960", "Mali": "+223", "Malte": "+356", "Îles Marshall": "+692",
	"Mauritanie": "+222", "Maurice": "+230", "Mexique": "+52", "Micronésie": "+691", "Moldavie": "+373", "Monaco": "+377",
	"Mongolie": "+976", "Monténégro": "+382", "Maroc": "+212", "Mozambique": "+258", "Myanmar": "+95", "Namibie": "+264", "Nauru": "+674",
	"Népal": "+977", "Pays-Bas": "+31", "Nouvelle-Zélande": "+64", "Nicaragua": "+505", "Niger": "+227", "Nigeria": "+234",
	"Macédoine du Nord": "+389", "Norvège": "+47", "Paraguay": "+595", "Pérou": "+51", "Philippines": "+63", "Pologne": "+48",
	"Portugal": "+351", "Qatar": "+974", "Roumanie": "+40", "Russie": "+7", "Rwanda": "+250", "Samoa": "+685", "Saint-Marin": "+378",
	"Sao Tomé-et-Principe": "+239", "Arabie saoudite": "+966", "Sénégal": "+221", "Serbie": "+381", "Seychelles": "+248", "Sierra Leone": "+232",
	"Singapour": "+65", "Slovaquie": "+421", "Slovénie": "+386", "Îles Salomon": "+677", "Somalie": "+252", "Afrique du Sud": "+27",
	"Sud-Soudan": "+211", "Espagne": "+34", "Sri Lanka": "+94", "Soudan": "+249", "Suriname": "+597", "Suède": "+46", "Suisse": "+41",
	"Syrie": "+963", "Tanzanie": "+255", "Thaïlande": "+66", "Togo": "+228", "Tonga": "+676", "Tunisie": "+216", "Turquie": "+90",
	"Ouganda": "+256", "Ukraine": "+380", "Émirats arabes unis": "+971", "Royaume-Uni": "+44", "États-Unis": "+1", "Uruguay": "+598",
	"Venezuela": "+58", "Yémen": "+967", "Zambie": "+260", "Zimbabwe": "+263"
	};

	var selectedCountry = this.value;
	var phoneCode = countryPhoneCodes[selectedCountry] || '';

	document.getElementById('coordonnees_tel').value = phoneCode;
});
